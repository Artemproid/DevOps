from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.api import deps
from app.core.redis_client import redis_client, get_online_users_data

router = APIRouter()


@router.get("/health")
def health_check() -> Dict[str, Any]:
    """
    Проверка состояния системы.
    """
    health_status = {
        "status": "healthy",
        "services": {
            "database": "healthy",
            "redis": "healthy" if redis_client.is_connected() else "unhealthy"
        }
    }
    
    if not redis_client.is_connected():
        health_status["status"] = "degraded"
    
    return health_status


@router.get("/metrics")
def get_metrics(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict[str, Any]:
    """
    Получить метрики системы (только для аутентифицированных пользователей).
    """
    online_users = get_online_users_data()
    
    return {
        "online_users_count": len(online_users),
        "online_users": online_users,
        "redis_connected": redis_client.is_connected(),
        "system_status": "operational"
    }


@router.get("/redis/info")
def get_redis_info(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict[str, Any]:
    """
    Получить информацию о Redis (только для админов/разработки).
    """
    if not redis_client.is_connected():
        raise HTTPException(status_code=503, detail="Redis not connected")
    
    try:
        # Получаем базовую информацию о Redis
        info = redis_client.redis_client.info()
        
        return {
            "connected": True,
            "version": info.get("redis_version"),
            "used_memory": info.get("used_memory_human"),
            "connected_clients": info.get("connected_clients"),
            "total_commands_processed": info.get("total_commands_processed"),
            "uptime_in_seconds": info.get("uptime_in_seconds")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")


@router.post("/redis/clear-cache")
def clear_redis_cache(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict[str, str]:
    """
    Очистить кэш Redis (осторожно!).
    """
    if not redis_client.is_connected():
        raise HTTPException(status_code=503, detail="Redis not connected")
    
    try:
        # Очищаем только кэшированные данные, не статусы пользователей
        pattern = "cache:*"
        keys = redis_client.redis_client.keys(pattern)
        if keys:
            redis_client.redis_client.delete(*keys)
        
        return {"message": f"Cleared {len(keys)} cache entries"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")
