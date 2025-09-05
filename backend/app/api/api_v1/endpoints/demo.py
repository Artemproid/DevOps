from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps

router = APIRouter()


@router.post("/activate-premium")
def demo_activate_premium(
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    🎭 DEMO: Активирует премиум для тестирования
    Используется только для демонстрации функциональности
    """
    
    # Активируем премиум для пользователя
    crud.crud_user.update_subscription(
        db, 
        current_user.id, 
        subscription_id="demo_subscription_123", 
        is_premium=True
    )
    
    return {
        "success": True,
        "message": "🏴‍☠️ Премиум активирован! Пиратский режим разблокирован!",
        "demo": True
    }


@router.post("/deactivate-premium")  
def demo_deactivate_premium(
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    🎭 DEMO: Деактивирует премиум для тестирования
    """
    
    # Деактивируем премиум
    crud.crud_user.update_subscription(
        db, 
        current_user.id, 
        subscription_id=None, 
        is_premium=False
    )
    
    return {
        "success": True,
        "message": "⚓ Премиум деактивирован. Пиратский режим заблокирован.",
        "demo": True
    }