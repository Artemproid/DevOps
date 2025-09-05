from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Chat])
def get_user_chats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить все чаты пользователя.
    """
    chats = crud.crud_chat.get_user_chats(db, current_user.id)
    return chats


@router.get("/detailed/")
def get_user_chats_detailed(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить детальную информацию о чатах пользователя с последними сообщениями.
    """
    chats = crud.crud_chat.get_user_chats_with_details(db, current_user.id)
    return chats


@router.get("/public/", response_model=schemas.Chat)
def get_public_chat(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить общий чат.
    """
    # Добавляем пользователя в общий чат если его там нет
    crud.crud_chat.add_user_to_public_chat(db, current_user.id)
    
    public_chat = crud.crud_chat.get_public_chat(db)
    return public_chat


@router.get("/private/{user_id}/", response_model=schemas.Chat)
def get_or_create_private_chat(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить или создать приватный чат с пользователем.
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot create chat with yourself"
        )
    
    # Проверяем, что пользователь существует
    target_user = crud.crud_user.get_user(db, user_id)
    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    chat = crud.crud_chat.get_or_create_private_chat(db, current_user.id, user_id)
    return chat


@router.get("/{chat_id}/", response_model=schemas.Chat)
def get_chat(
    chat_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить информацию о чате.
    """
    chat = crud.crud_chat.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
    
    # Проверяем, что пользователь является участником чата
    if not crud.crud_chat.is_user_in_chat(db, current_user.id, chat_id):
        raise HTTPException(
            status_code=403,
            detail="You are not a participant of this chat"
        )
    
    return chat
