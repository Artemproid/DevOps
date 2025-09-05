"""
🏴‍☠️ API ЭНДПОИНТ ДЛЯ ПИРАТСКОЙ СТИЛИЗАЦИИ

Обрабатывает запросы на стилизацию текста под пиратскую речь
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.services.pirate_service import pirate_transformer
from app.api import deps
from app import models

router = APIRouter()

class PirateRequest(BaseModel):
    text: str
    style: Optional[str] = "pirate"

class PirateResponse(BaseModel):
    original_text: str
    pirate_text: str
    style: str
    success: bool

@router.post("/transform", response_model=PirateResponse)
async def transform_to_pirate(
    request: PirateRequest,
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    Преобразует обычный текст в пиратский стиль
    
    - **text**: Исходный текст для преобразования
    - **style**: Стиль (пока только "pirate")
    
    🏴‍☠️ ТРЕБУЕТ ПРЕМИУМ ПОДПИСКУ!
    """
    
    try:
        # Проверяем премиум статус
        if not current_user.is_premium:
            raise HTTPException(
                status_code=403, 
                detail="🚫 Пиратский режим доступен только для премиум пользователей! Оформите подписку в /api/payments/create-checkout-session"
            )
        
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="Текст не может быть пустым")
        
        # Преобразуем текст с помощью LLM (с fallback к regex)
        pirate_text = await pirate_transformer.transform_with_llm(request.text)
        
        return PirateResponse(
            original_text=request.text,
            pirate_text=pirate_text,
            style=request.style,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка преобразования: {str(e)}")

@router.get("/pirate/exclamation")
async def get_exclamation():
    """
    Возвращает случайное пиратское восклицание
    """
    
    try:
        # Получаем случайное восклицание
        import random
        exclamations = ["Arr!", "Йо-хо-хо!", "Тысяча чертей!", "Кальмарьи кишки!", "Разрази меня гром!"]
        exclamation = random.choice(exclamations)
        return {
            "exclamation": exclamation,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения восклицания: {str(e)}")

@router.get("/pirate/test")
async def test_pirate_service():
    """
    Тестирует работу пиратского сервиса
    """
    
    test_phrases = [
        "Привет, как дела?",
        "Иду спать",
        "Хочу есть", 
        "Нужны деньги",
        "До свидания"
    ]
    
    results = []
    
    for phrase in test_phrases:
        try:
            pirate_text = pirate_transformer.transform(phrase)
            results.append({
                "original": phrase,
                "pirate": pirate_text,
                "success": True
            })
        except Exception as e:
            results.append({
                "original": phrase,
                "pirate": None,
                "success": False,
                "error": str(e)
            })
    
    # Получаем случайное восклицание
    import random
    exclamations = ["Arr!", "Йо-хо-хо!", "Тысяча чертей!", "Кальмарьи кишки!", "Разрази меня гром!"]
    exclamation = random.choice(exclamations)
    
    return {
        "test_results": results,
        "total_tests": len(test_phrases),
        "success_count": len([r for r in results if r["success"]]),
        "exclamation": exclamation
    }
