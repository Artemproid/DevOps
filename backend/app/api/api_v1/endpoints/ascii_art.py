"""
ASCII Art API endpoints
"""

import logging
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app import models
from app.api import deps
from app.services.ascii_art_service import ascii_art_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic модели
class ASCIIArtRequest(BaseModel):
    text: str
    font: str = "slant"

class ASCIIArtResponse(BaseModel):
    ascii_art: str
    font: str
    original_text: str

class FontPreviewResponse(BaseModel):
    fonts: Dict[str, str]

@router.post("/generate", response_model=ASCIIArtResponse)
async def generate_ascii_art(
    request: ASCIIArtRequest,
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    Генерирует ASCII арт из текста (только для premium пользователей)
    """
    try:
        # Проверяем premium статус
        if not current_user.is_premium:
            raise HTTPException(
                status_code=403, 
                detail="🎨 ASCII арт доступен только для Premium пользователей! Оформите подписку."
            )
        
        # Валидация текста
        is_valid, error_msg = ascii_art_service.validate_text(request.text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"❌ {error_msg}")
        
        # Генерируем ASCII арт
        ascii_art = ascii_art_service.generate_ascii_art(
            text=request.text.strip(), 
            font=request.font
        )
        
        if not ascii_art:
            raise HTTPException(
                status_code=500, 
                detail="❌ Ошибка генерации ASCII арт. Попробуйте другой шрифт."
            )
        
        # DEBUG: Логируем что отправляем
        newline = '\n'
        print(f"🌐 DEBUG API Response:")
        print(f"  ASCII length: {len(ascii_art)}")
        print(f"  Has newlines: {newline in ascii_art}")
        print(f"  Lines count: {len(ascii_art.split(newline))}")
        print(f"  First 100 chars: {ascii_art[:100]!r}")
        
        logger.info(f"🎨 User {current_user.username} создал ASCII арт: '{request.text}'")
        
        return ASCIIArtResponse(
            ascii_art=ascii_art,
            font=request.font,
            original_text=request.text
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Ошибка в generate_ascii_art: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/fonts", response_model=FontPreviewResponse)
async def get_available_fonts(
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    Получить список доступных шрифтов с превью
    """
    try:
        # Проверяем premium статус
        if not current_user.is_premium:
            raise HTTPException(
                status_code=403, 
                detail="🎨 Превью шрифтов доступно только для Premium пользователей!"
            )
        
        fonts_with_previews = ascii_art_service.get_available_fonts_with_previews()
        
        return FontPreviewResponse(fonts=fonts_with_previews)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Ошибка в get_available_fonts: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/demo")
async def demo_ascii_art():
    """
    Демо ASCII арт для всех пользователей (без авторизации)
    """
    try:
        demo_art = ascii_art_service.generate_ascii_art("DEMO", "slant")
        
        return {
            "ascii_art": demo_art,
            "message": "🎨 Вот что может ASCII арт! Оформите Premium для полного доступа.",
            "premium_required": True
        }
        
    except Exception as e:
        logger.error(f"❌ Ошибка в demo_ascii_art: {e}")
        return {
            "ascii_art": "ERROR",
            "message": "Ошибка демо",
            "premium_required": True
        }