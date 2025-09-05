import redis
import json
import logging
import os
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)

class RedisClient:
    """Redis клиент для межсервисной коммуникации"""
    
    def __init__(self):
        self.redis_client = None
        self.connect()
    
    def connect(self):
        """Подключение к Redis"""
        try:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'redis'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            # Тестируем соединение
            self.redis_client.ping()
            logger.info("✅ Redis connected successfully")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.redis_client = None
    
    def is_connected(self) -> bool:
        """Проверка подключения к Redis"""
        try:
            return self.redis_client is not None and self.redis_client.ping()
        except:
            return False
    
    # ===== PUB/SUB для событий =====
    
    def publish_event(self, channel: str, event_type: str, data: Dict[str, Any]) -> bool:
        """Публикация события"""
        if not self.is_connected():
            logger.warning("Redis not connected, skipping event publication")
            return False
        
        try:
            message = {
                "event_type": event_type,
                "data": data,
                "timestamp": str(int(time.time()))
            }
            result = self.redis_client.publish(channel, json.dumps(message))
            logger.info(f"📡 Published event '{event_type}' to channel '{channel}' (subscribers: {result})")
            return True
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            return False
    
    def subscribe_to_channel(self, channel: str, callback):
        """Подписка на канал"""
        if not self.is_connected():
            logger.warning("Redis not connected, cannot subscribe")
            return None
        
        try:
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe(channel)
            logger.info(f"📨 Subscribed to channel '{channel}'")
            
            for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        callback(data)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
            
            return pubsub
        except Exception as e:
            logger.error(f"Failed to subscribe: {e}")
            return None
    
    # ===== Кэширование =====
    
    def set_cache(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Сохранение в кэш"""
        if not self.is_connected():
            return False
        
        try:
            serialized_value = json.dumps(value) if not isinstance(value, str) else value
            return self.redis_client.setex(key, expire, serialized_value)
        except Exception as e:
            logger.error(f"Failed to set cache: {e}")
            return False
    
    def get_cache(self, key: str) -> Optional[Any]:
        """Получение из кэша"""
        if not self.is_connected():
            return None
        
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            
            # Пытаемся распарсить JSON, если не получается - возвращаем как строку
            try:
                return json.loads(value)
            except:
                return value
        except Exception as e:
            logger.error(f"Failed to get cache: {e}")
            return None
    
    def delete_cache(self, key: str) -> bool:
        """Удаление из кэша"""
        if not self.is_connected():
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Failed to delete cache: {e}")
            return False
    
    # ===== Управление сессиями и онлайн статусами =====
    
    def set_user_online(self, user_id: int, username: str) -> bool:
        """Отметить пользователя как онлайн"""
        if not self.is_connected():
            return False
        
        try:
            # Добавляем в set онлайн пользователей
            self.redis_client.sadd("online_users", user_id)
            
            # Сохраняем данные пользователя
            self.redis_client.setex(f"user:{user_id}:data", 3600, json.dumps({
                "id": user_id,
                "username": username,
                "status": "online",
                "last_seen": str(int(time.time()))
            }))
            
            return True
        except Exception as e:
            logger.error(f"Failed to set user online: {e}")
            return False
    
    def set_user_offline(self, user_id: int) -> bool:
        """Отметить пользователя как оффлайн"""
        if not self.is_connected():
            return False
        
        try:
            # Убираем из set онлайн пользователей
            self.redis_client.srem("online_users", user_id)
            
            # Обновляем статус
            user_data = self.get_cache(f"user:{user_id}:data")
            if user_data:
                user_data["status"] = "offline"
                user_data["last_seen"] = str(int(time.time()))
                self.set_cache(f"user:{user_id}:data", user_data, 86400)  # Храним оффлайн статус дольше
            
            return True
        except Exception as e:
            logger.error(f"Failed to set user offline: {e}")
            return False
    
    def get_online_users(self) -> list:
        """Получить список ID онлайн пользователей"""
        if not self.is_connected():
            return []
        
        try:
            user_ids = self.redis_client.smembers("online_users")
            return [int(uid) for uid in user_ids]
        except Exception as e:
            logger.error(f"Failed to get online users: {e}")
            return []
    
    def get_online_users_data(self) -> list:
        """Получить данные онлайн пользователей"""
        if not self.is_connected():
            return []
        
        try:
            user_ids = self.get_online_users()
            users_data = []
            
            for user_id in user_ids:
                user_data = self.get_cache(f"user:{user_id}:data")
                if user_data:
                    users_data.append(user_data)
            
            return users_data
        except Exception as e:
            logger.error(f"Failed to get online users data: {e}")
            return []


# Импорт time для timestamp
import time

# Singleton instance
redis_client = RedisClient()

# Convenience functions
def publish_event(channel: str, event_type: str, data: Dict[str, Any]) -> bool:
    return redis_client.publish_event(channel, event_type, data)

def set_user_online(user_id: int, username: str) -> bool:
    return redis_client.set_user_online(user_id, username)

def set_user_offline(user_id: int) -> bool:
    return redis_client.set_user_offline(user_id)

def get_online_users() -> list:
    return redis_client.get_online_users()

def get_online_users_data() -> list:
    return redis_client.get_online_users_data()
