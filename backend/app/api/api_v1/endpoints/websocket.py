import json
import asyncio
from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.core.websocket import manager
from app import crud, models
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="JWT токен для аутентификации")
):
    """WebSocket endpoint для real-time чата"""
    
    # Создаём сессию БД
    from app.db.session import SessionLocal
    db = SessionLocal()
    
    try:
        # Аутентификация пользователя по токену ПЕРЕД accept
        current_user = await get_current_user_from_token(token, db)
        if not current_user:
            logger.error("Invalid token provided")
            await websocket.close(code=4001, reason="Invalid token")
            return
            
        logger.info(f"User {current_user.id} authenticated, accepting WebSocket")
        
        # Принимаем соединение только после успешной аутентификации
        await websocket.accept()
        
        user_id = current_user.id
        
        # Подключаем пользователя
        await manager.connect(websocket, user_id, current_user.username)
        
        # Основной цикл
        while True:
            try:
                # Получаем сообщение от клиента
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                await handle_websocket_message(user_id, message_data, db)
                
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnect for user {user_id}")
                break
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from user {user_id}")
                continue
            except Exception as e:
                logger.error(f"Error handling message for user {user_id}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}", exc_info=True)
        try:
            await websocket.close(code=4000, reason="Connection error")
        except Exception as close_error:
            logger.error(f"Error closing websocket: {close_error}")
    finally:
        # Очищаем ресурсы
        if 'user_id' in locals() and 'current_user' in locals():
            await manager.disconnect(user_id, current_user.username)
        db.close()


async def handle_websocket_message(user_id: int, message_data: dict, db: Session):
    """Обработка сообщений от клиента"""
    
    message_type = message_data.get("type")
    
    if message_type == "join_chat":
        # Присоединение к чату
        chat_id = message_data.get("chat_id")
        if chat_id:
            # Проверяем права доступа к чату
            if crud.crud_chat.is_user_in_chat(db, user_id, chat_id):
                await manager.join_chat(user_id, chat_id)
                
                # Отправляем подтверждение
                await manager.send_personal_message(user_id, {
                    "type": "chat_joined",
                    "chat_id": chat_id
                })
    
    elif message_type == "leave_chat":
        # Покидание чата
        chat_id = message_data.get("chat_id")
        if chat_id:
            await manager.leave_chat(user_id, chat_id)
    
    elif message_type == "typing_start":
        # Начало печатания
        chat_id = message_data.get("chat_id")
        if chat_id:
            await manager.set_typing_status(user_id, chat_id, True)
    
    elif message_type == "typing_stop":
        # Остановка печатания
        chat_id = message_data.get("chat_id")
        if chat_id:
            await manager.set_typing_status(user_id, chat_id, False)
    
    elif message_type == "send_message":
        # Отправка сообщения (может быть заменено на обычный HTTP API)
        chat_id = message_data.get("chat_id")
        content = message_data.get("content")
        
        if chat_id and content:
            # Проверяем права
            if crud.crud_chat.is_user_in_chat(db, user_id, chat_id):
                # Создаём сообщение через CRUD
                from app.schemas.message import MessageCreate
                message_in = MessageCreate(content=content, chat_id=chat_id)
                new_message = crud.crud_message.create_message(db, message_in, user_id)
                
                # Конвертируем в JSON-совместимый формат
                message_dict = {
                    "id": new_message.id,
                    "content": new_message.content,
                    "created_at": new_message.created_at.isoformat(),
                    "user_id": new_message.user_id,
                    "chat_id": new_message.chat_id,
                    "user": {
                        "id": new_message.user.id,
                        "username": new_message.user.username,
                        "email": new_message.user.email
                    }
                }
                
                # Рассылаем сообщение участникам чата
                await manager.broadcast_new_message(chat_id, message_dict)
    
    elif message_type == "get_online_users":
        # Запрос списка онлайн пользователей
        online_user_ids = manager.get_online_users()
        
        # Получаем данные пользователей
        online_users_data = []
        for uid in online_user_ids:
            if uid != user_id:  # Исключаем себя
                user = crud.crud_user.get_user(db, user_id=uid)
                if user:
                    online_users_data.append({
                        "id": user.id,
                        "username": user.username
                    })
        
        await manager.send_personal_message(user_id, {
            "type": "online_users",
            "users": online_users_data
        })


async def get_current_user_from_token(token: str, db: Session) -> models.User:
    """Получение пользователя по токену (для WebSocket)"""
    from jose import jwt, JWTError
    from app.core.security import SECRET_KEY, ALGORITHM
    from app import schemas
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            return None
        token_data = schemas.TokenPayload(sub=user_id)
    except (JWTError, ValueError):
        return None
    
    user = crud.crud_user.get_user(db, user_id=token_data.sub)
    return user
