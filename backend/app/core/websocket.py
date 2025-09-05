import json
import asyncio
from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import logging
from app.core.redis_client import redis_client, publish_event, set_user_online, set_user_offline

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # Активные соединения: {user_id: WebSocket}
        self.active_connections: Dict[int, WebSocket] = {}
        
        # Пользователи в чатах: {chat_id: Set[user_id]}
        self.chat_participants: Dict[int, Set[int]] = {}
        
        # Статус печатания: {chat_id: {user_id: True}}
        self.typing_users: Dict[int, Dict[int, bool]] = {}
        
        # Онлайн пользователи
        self.online_users: Set[int] = set()

    async def connect(self, websocket: WebSocket, user_id: int, username: str = None):
        """Подключение пользователя"""
        # WebSocket уже принят в эндпоинте, не нужно accept() здесь
        
        # Если пользователь уже подключен, отключаем старое соединение
        if user_id in self.active_connections:
            try:
                old_websocket = self.active_connections[user_id]
                if old_websocket.client_state.name == "CONNECTED":
                    await old_websocket.close(code=1000, reason="New connection")
            except Exception as e:
                logger.error(f"Error closing old connection for user {user_id}: {e}")
        
        self.active_connections[user_id] = websocket
        self.online_users.add(user_id)
        
        # Сохраняем статус в Redis
        if username:
            set_user_online(user_id, username)
            
        logger.info(f"User {user_id} connected successfully")
        
        # Публикуем событие в Redis
        try:
            publish_event("user_events", "user_connected", {
                "user_id": user_id,
                "username": username,
                "timestamp": str(int(asyncio.get_event_loop().time()))
            })
        except Exception as e:
            logger.error(f"Error publishing user connected event: {e}")
        
        # Уведомляем других о том, что пользователь онлайн (только если соединение активно)
        try:
            if websocket.client_state.name == "CONNECTED":
                await self.broadcast_user_status(user_id, "online", username)
        except Exception as e:
            logger.error(f"Error broadcasting online status for user {user_id}: {e}")
            # Если не можем отправить статус - отключаем пользователя
            await self.disconnect(user_id, username)

    async def disconnect(self, user_id: int, username: str = None):
        """Отключение пользователя"""
        # Закрываем WebSocket соединение если нужно
        if user_id in self.active_connections:
            try:
                websocket = self.active_connections[user_id]
                if websocket.client_state.name != "DISCONNECTED":
                    await websocket.close(code=1000, reason="Server disconnect")
            except Exception as e:
                logger.error(f"Error closing websocket for user {user_id}: {e}")
            finally:
                del self.active_connections[user_id]
        
        self.online_users.discard(user_id)
        
        # Обновляем статус в Redis
        set_user_offline(user_id)
        
        # Убираем из всех чатов
        for chat_id in list(self.chat_participants.keys()):
            self.chat_participants[chat_id].discard(user_id)
            if not self.chat_participants[chat_id]:
                del self.chat_participants[chat_id]
        
        # Убираем из типинга
        for chat_id in self.typing_users:
            self.typing_users[chat_id].pop(user_id, None)
        
        logger.info(f"User {user_id} disconnected")
        
        # Публикуем событие в Redis
        try:
            publish_event("user_events", "user_disconnected", {
                "user_id": user_id,
                "username": username,
                "timestamp": str(int(asyncio.get_event_loop().time()))
            })
        except Exception as e:
            logger.error(f"Error publishing user disconnected event: {e}")
        
        # Уведомляем других о том, что пользователь офлайн
        try:
            await self.broadcast_user_status(user_id, "offline", username)
        except Exception as e:
            logger.error(f"Error broadcasting offline status for user {user_id}: {e}")

    async def join_chat(self, user_id: int, chat_id: int):
        """Присоединение к чату"""
        if chat_id not in self.chat_participants:
            self.chat_participants[chat_id] = set()
        
        self.chat_participants[chat_id].add(user_id)
        logger.info(f"User {user_id} joined chat {chat_id}")

    async def leave_chat(self, user_id: int, chat_id: int):
        """Покидание чата"""
        if chat_id in self.chat_participants:
            self.chat_participants[chat_id].discard(user_id)
            if not self.chat_participants[chat_id]:
                del self.chat_participants[chat_id]
        
        # Убираем из типинга
        if chat_id in self.typing_users:
            self.typing_users[chat_id].pop(user_id, None)
        
        logger.info(f"User {user_id} left chat {chat_id}")

    async def send_personal_message(self, user_id: int, message: dict):
        """Отправка сообщения конкретному пользователю"""
        if user_id in self.active_connections:
            try:
                websocket = self.active_connections[user_id]
                # Проверяем состояние соединения
                if websocket.client_state.name == "CONNECTED":
                    await websocket.send_text(json.dumps(message))
                else:
                    logger.warning(f"WebSocket for user {user_id} is not connected")
                    await self.disconnect(user_id)
            except Exception as e:
                logger.error(f"Error sending message to user {user_id}: {e}")
                await self.disconnect(user_id)

    async def broadcast_to_chat(self, chat_id: int, message: dict, exclude_user: int = None):
        """Рассылка сообщения всем участникам чата"""
        if chat_id not in self.chat_participants:
            return
        
        participants = self.chat_participants[chat_id].copy()
        if exclude_user:
            participants.discard(exclude_user)
        
        disconnected_users = []
        
        for user_id in participants:
            if user_id in self.active_connections:
                try:
                    websocket = self.active_connections[user_id]
                    await websocket.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error broadcasting to user {user_id}: {e}")
                    disconnected_users.append(user_id)
        
        # Удаляем отключившихся пользователей
        for user_id in disconnected_users:
            await self.disconnect(user_id)

    async def set_typing_status(self, user_id: int, chat_id: int, is_typing: bool):
        """Установка статуса печатания"""
        if chat_id not in self.typing_users:
            self.typing_users[chat_id] = {}
        
        if is_typing:
            self.typing_users[chat_id][user_id] = True
        else:
            self.typing_users[chat_id].pop(user_id, None)
        
        # Отправляем обновление статуса другим участникам
        typing_list = list(self.typing_users[chat_id].keys())
        message = {
            "type": "typing_update",
            "chat_id": chat_id,
            "typing_users": typing_list
        }
        
        await self.broadcast_to_chat(chat_id, message, exclude_user=user_id)

    async def broadcast_user_status(self, user_id: int, status: str, username: str = None):
        """Рассылка статуса пользователя (online/offline)"""
        message = {
            "type": "user_status",
            "user_id": user_id,
            "username": username,
            "status": status
        }
        
        # Отправляем всем онлайн пользователям
        for online_user_id in list(self.online_users):
            if online_user_id != user_id:
                await self.send_personal_message(online_user_id, message)

    async def broadcast_new_message(self, chat_id: int, message_data: dict):
        """Рассылка нового сообщения участникам чата"""
        message = {
            "type": "new_message",
            "chat_id": chat_id,
            "message": message_data
        }
        
        await self.broadcast_to_chat(chat_id, message)

    def get_online_users(self) -> List[int]:
        """Получить список онлайн пользователей"""
        return list(self.online_users)

    def is_user_online(self, user_id: int) -> bool:
        """Проверить, онлайн ли пользователь"""
        return user_id in self.online_users


# Глобальный менеджер соединений
manager = ConnectionManager()
