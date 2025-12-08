"""
🏭 Фабрика сообщений - Factory Pattern для разных типов сообщений
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import re


class MessageProcessor(ABC):
    """Абстрактный базовый класс для обработки сообщений"""
    
    @abstractmethod
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """Обрабатывает сообщение и возвращает данные для сохранения"""
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        """Возвращает тип сообщения"""
        pass


class RegularMessageProcessor(MessageProcessor):
    """Обработчик обычных сообщений"""
    
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        return {
            "content": content.strip(),
            "message_type": self.get_type()
        }
    
    def get_type(self) -> str:
        return "normal"


class ASCIIArtMessageProcessor(MessageProcessor):
    """Обработчик ASCII арт сообщений"""
    
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        # Сохраняем форматирование для ASCII арт
        return {
            "content": content,  # Не убираем пробелы!
            "message_type": self.get_type()
        }
    
    def get_type(self) -> str:
        return "ascii_art"
    
    @staticmethod
    def is_ascii_art(content: str) -> bool:
        """Определяет, является ли сообщение ASCII артом"""
        ascii_patterns = [
            r'[╔╗╚╝═║┌┐└┘─│]',  # Символы рамок
            r'[▄▀█▌▐]',          # Блочные символы
            r'[/\\|_-]{3,}',     # Понижен порог с 5 до 3
            r'\s+[_/\\|]{2,}',   # ASCII символы с пробелами
        ]
        
        # Проверяем наличие ASCII символов (понижен порог)
        for pattern in ascii_patterns:
            if len(re.findall(pattern, content)) >= 1:
                return True
        
        # Проверяем на характерные последовательности
        if re.search(r'[_/\\|-]{4,}', content):
            return True
            
        if re.search(r'\s+[_/\\|]{2,}\s+', content):
            return True
        
        # Проверяем многострочность с ASCII символами (понижен порог)
        lines = content.split('\n')
        if len(lines) >= 2:
            ascii_lines = sum(1 for line in lines 
                            if re.search(r'[_/\\|+\-=<>(){}[\]]{3,}', line) 
                            and len(line.strip()) > 3)
            if ascii_lines >= 1:
                return True
        
        return False


class SystemMessageProcessor(MessageProcessor):
    """Обработчик системных сообщений"""
    
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        return {
            "content": f"🤖 СИСТЕМА: {content.strip()}",
            "message_type": self.get_type()
        }
    
    def get_type(self) -> str:
        return "system"


class MessageFactory:
    """🏭 Фабрика для создания сообщений разных типов"""
    
    def __init__(self):
        self._processors = {
            "normal": RegularMessageProcessor(),
            "ascii_art": ASCIIArtMessageProcessor(),
            "system": SystemMessageProcessor(),
        }
    
    def create_message_data(
        self, 
        content: str, 
        message_type: Optional[str] = None,
        auto_detect: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создает данные для сообщения с автоопределением типа
        
        Args:
            content: Содержимое сообщения
            message_type: Явно указанный тип (опционально)
            auto_detect: Автоопределение типа сообщения
            **kwargs: Дополнительные параметры
        
        Returns:
            Словарь с данными для создания сообщения
        """
        # Автоопределение типа, если не указан явно
        if message_type is None and auto_detect:
            message_type = self._detect_message_type(content)
        elif message_type is None:
            message_type = "normal"
        
        # Получаем соответствующий процессор
        processor = self._processors.get(message_type, self._processors["normal"])
        
        # Обрабатываем сообщение
        return processor.process(content, **kwargs)
    
    def _detect_message_type(self, content: str) -> str:
        """Автоматически определяет тип сообщения"""
        # Проверяем на ASCII арт
        if ASCIIArtMessageProcessor.is_ascii_art(content):
            return "ascii_art"
        
        # Проверяем на системные сообщения (начинаются с префиксов)
        content_lower = content.lower().strip()
        if any(content_lower.startswith(prefix) for prefix in ['система:', 'system:', '🤖']):
            return "system"
        
        # По умолчанию - обычное сообщение
        return "normal"
    
    def get_available_types(self) -> list[str]:
        """Возвращает список доступных типов сообщений"""
        return list(self._processors.keys())


# Синглтон фабрики
message_factory = MessageFactory()
