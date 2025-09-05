from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.services.message_factory import message_factory

router = APIRouter()


@router.get("/", response_model=List[schemas.Message])
def read_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve public chat messages (backward compatibility).
    """
    # Добавляем пользователя в общий чат если его там нет
    crud.crud_chat.add_user_to_public_chat(db, current_user.id)
    
    messages = crud.crud_message.get_messages(db, skip=skip, limit=limit)
    return messages


@router.get("/chat/{chat_id}/", response_model=List[schemas.Message])
def get_chat_messages(
    chat_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить сообщения конкретного чата.
    """
    # Проверяем, что пользователь является участником чата
    if not crud.crud_chat.is_user_in_chat(db, current_user.id, chat_id):
        raise HTTPException(
            status_code=403,
            detail="You are not a participant of this chat"
        )
    
    messages = crud.crud_message.get_chat_messages(db, chat_id=chat_id, skip=skip, limit=limit)
    return messages


@router.get("/private/{user_id}/", response_model=List[schemas.Message])
def get_private_messages(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить приватные сообщения с конкретным пользователем.
    """
    # Получаем или создаём приватный чат
    chat = crud.crud_chat.get_or_create_private_chat(db, current_user.id, user_id)
    
    messages = crud.crud_message.get_chat_messages(db, chat_id=chat.id, skip=skip, limit=limit)
    return messages


@router.post("/", response_model=schemas.Message)
async def create_message(
    *,
    message_in: schemas.MessageCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new message using Factory Pattern.
    """
    # Проверяем, что пользователь является участником чата
    if not crud.crud_chat.is_user_in_chat(db, current_user.id, message_in.chat_id):
        raise HTTPException(
            status_code=403,
            detail="You are not a participant of this chat"
        )
    
    # 🔍 ДЕБАГ: Проверяем содержимое до обработки
    newline_char = '\n'
    print(f"🔍 ВХОД MESSAGE:")
    print(f"  Content length: {len(message_in.content)}")
    print(f"  Has newlines: {newline_char in message_in.content}")
    print(f"  Content repr: {repr(message_in.content[:200])}")
    print(f"  Message type: {message_in.message_type}")
    
    # 🏭 Используем фабрику для обработки сообщения
    processed_data = message_factory.create_message_data(
        content=message_in.content,
        message_type=message_in.message_type,
        auto_detect=True
    )
    
    # 🔍 ДЕБАГ: Проверяем содержимое после обработки
    print(f"🔍 ОБРАБОТКА ФАБРИКИ:")
    print(f"  Processed type: {processed_data['message_type']}")
    print(f"  Processed content length: {len(processed_data['content'])}")
    print(f"  Processed has newlines: {newline_char in processed_data['content']}")
    print(f"  Processed repr: {repr(processed_data['content'][:200])}")
    
    # Обновляем данные сообщения
    message_in.content = processed_data["content"]
    message_in.message_type = processed_data["message_type"]
    
    message = crud.crud_message.create_message(
        db=db, message_in=message_in, user_id=current_user.id
    )
    
    # Отправляем real-time уведомление через WebSocket
    from app.core.websocket import manager
    message_dict = {
        "id": message.id,
        "content": message.content,
        "message_type": message.message_type.value,  # Добавляем тип сообщения
        "created_at": message.created_at.isoformat(),
        "user_id": message.user_id,
        "chat_id": message.chat_id,
        "user": {
            "id": message.user.id,
            "username": message.user.username,
            "email": message.user.email
        }
    }
    
    await manager.broadcast_new_message(message_in.chat_id, message_dict)
    
    return message 