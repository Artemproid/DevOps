"""
ASCII Art Generator Service
Превращает текст в красивые ASCII картинки
"""

import logging
from typing import Optional, List, Dict
from pyfiglet import Figlet, FigletFont

logger = logging.getLogger(__name__)

class ASCIIArtService:
    """Сервис для генерации ASCII арт"""
    
    def __init__(self):
        self.popular_fonts = [
            'slant',
            'banner',
            'big',
            'block',
            'bubble',
            'digital',
            'isometric1',
            'letters',
            'alligator',
            'doom'
        ]
        
        # Инициализируем доступные шрифты
        self.available_fonts = self._get_available_fonts()
        logger.info(f"🎨 ASCII Art сервис загружен с {len(self.available_fonts)} шрифтами")
    
    def _get_available_fonts(self) -> List[str]:
        """Получаем список доступных шрифтов"""
        try:
            # Получаем все доступные шрифты
            all_fonts = FigletFont.getFonts()
            
            # Фильтруем популярные шрифты которые точно есть
            available = []
            for font in self.popular_fonts:
                if font in all_fonts:
                    available.append(font)
            
            # Добавляем еще несколько случайных если мало
            if len(available) < 5:
                for font in all_fonts[:10]:
                    if font not in available:
                        available.append(font)
                        if len(available) >= 10:
                            break
                            
            return available
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения шрифтов: {e}")
            return ['slant', 'banner', 'big']  # Fallback шрифты
    
    def generate_ascii_art(self, text: str, font: str = 'slant') -> Optional[str]:
        """
        Генерирует ASCII арт из текста
        
        Args:
            text: Текст для преобразования
            font: Шрифт для ASCII арт
            
        Returns:
            ASCII арт строка или None при ошибке
        """
        try:
            # Ограничиваем длину текста
            if len(text) > 50:
                text = text[:50]
            
            # Проверяем доступность шрифта
            if font not in self.available_fonts:
                font = 'slant'  # Дефолтный шрифт
                
            # Создаем ASCII арт
            figlet = Figlet(font=font)
            ascii_art = figlet.renderText(text)
            
            # DEBUG: Логируем что получили
            newline = '\n'
            print(f"🎨 DEBUG ASCII Generated:")
            print(f"  Text: '{text}'")
            print(f"  Font: '{font}'")
            print(f"  Length: {len(ascii_art)}")
            print(f"  Has newlines: {newline in ascii_art}")
            print(f"  Lines count: {len(ascii_art.split(newline))}")
            print(f"  First 100 chars: {ascii_art[:100]!r}")
            
            logger.info(f"✅ Создан ASCII арт для '{text}' шрифтом '{font}'")
            return ascii_art
            
        except Exception as e:
            logger.error(f"❌ Ошибка генерации ASCII арт: {e}")
            return None
    
    def get_font_preview(self, font: str, sample_text: str = "ABC") -> Optional[str]:
        """
        Показывает превью шрифта
        
        Args:
            font: Название шрифта
            sample_text: Образец текста для превью
            
        Returns:
            Превью ASCII арт
        """
        try:
            if font not in self.available_fonts:
                return None
                
            figlet = Figlet(font=font)
            preview = figlet.renderText(sample_text)
            return preview
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания превью: {e}")
            return None
    
    def get_available_fonts_with_previews(self) -> Dict[str, str]:
        """
        Возвращает словарь доступных шрифтов с превью
        
        Returns:
            Словарь {font_name: preview_text}
        """
        fonts_with_previews = {}
        
        for font in self.available_fonts[:8]:  # Берем первые 8 шрифтов
            preview = self.get_font_preview(font, "Hi")
            if preview:
                fonts_with_previews[font] = preview
                
        return fonts_with_previews
    
    def validate_text(self, text: str) -> tuple[bool, str]:
        """
        Валидация текста для ASCII арт
        
        Args:
            text: Текст для проверки
            
        Returns:
            (is_valid, error_message)
        """
        if not text or not text.strip():
            return False, "Текст не может быть пустым"
            
        if len(text) > 50:
            return False, "Текст слишком длинный (максимум 50 символов)"
            
        # Проверяем что текст содержит только ASCII символы
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False, "Текст должен содержать только английские символы и цифры"
            
        return True, ""

# Глобальный экземпляр сервиса
ascii_art_service = ASCIIArtService()
