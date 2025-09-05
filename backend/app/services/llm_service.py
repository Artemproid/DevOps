"""
LLM Service - Русская GPT-2 для трансформации текста
"""

import os
import logging
import torch
from typing import Optional, List
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class LLMTextTransformer:
    """Сервис для трансформации текста с помощью русской GPT-2"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.model_path = "/app/models/rus_gpt2"
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.initialized = False
        
        # Инициализируем асинхронно
        self._initialize_model()
    
    def _initialize_model(self):
        """Инициализация модели"""
        try:
            logger.info("🧠 Загружаем русскую GPT-2 модель...")
            
            # Проверяем доступность модели
            if not os.path.exists(self.model_path):
                logger.error(f"❌ Модель не найдена по пути: {self.model_path}")
                return
            
            # Загружаем токенайзер
            self.tokenizer = GPT2Tokenizer.from_pretrained(
                self.model_path,
                padding_side='left'
            )
            
            # Устанавливаем pad_token если его нет
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Загружаем модель
            self.model = GPT2LMHeadModel.from_pretrained(
                self.model_path,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )
            
            # Переводим в eval режим
            self.model.eval()
            
            # Создаем pipeline для удобства
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1,  # CPU
                return_full_text=False,
                do_sample=True,
                temperature=0.8,
                top_p=0.9,
                max_new_tokens=100,
                repetition_penalty=1.1
            )
            
            self.initialized = True
            logger.info("✅ Русская GPT-2 модель загружена успешно!")
            
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки модели: {e}")
            self.initialized = False
    
    async def transform_to_pirate(self, text: str) -> Optional[str]:
        """
        Трансформирует текст в пиратский стиль с помощью GPT-2
        """
        if not self.initialized:
            logger.warning("⚠️ Модель не загружена, используем fallback")
            return self._fallback_pirate_transform(text)
        
        try:
            # Создаем промпт для пиратской трансформации
            prompt = self._create_pirate_prompt(text)
            
            # Запускаем генерацию в отдельном потоке
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                self._generate_text, 
                prompt
            )
            
            if result:
                # Извлекаем только пиратскую часть
                pirate_text = self._extract_pirate_response(result, text)
                logger.info(f"🏴‍☠️ LLM трансформация: '{text}' -> '{pirate_text}'")
                return pirate_text
            else:
                return self._fallback_pirate_transform(text)
                
        except Exception as e:
            logger.error(f"❌ Ошибка LLM трансформации: {e}")
            return self._fallback_pirate_transform(text)
    
    async def transform_to_style(self, text: str, style: str = "pirate") -> Optional[str]:
        """
        Универсальная трансформация в разные стили
        """
        if style == "pirate":
            return await self.transform_to_pirate(text)
        elif style == "knight":
            return await self.transform_to_knight(text)
        elif style == "robot":
            return await self.transform_to_robot(text)
        else:
            return text
    
    async def transform_to_knight(self, text: str) -> Optional[str]:
        """Трансформация в рыцарский стиль"""
        if not self.initialized:
            return text + " Честь и доблесть!"
        
        try:
            prompt = f"""Переведи обычную речь в речь средневекового рыцаря:

Обычно: Привет, как дела?
Рыцарски: Приветствую вас, милорд! Как поживаете?

Обычно: Пойдем поедим
Рыцарски: Предлагаю отправиться на пиршество в великий зал!

Обычно: {text}
Рыцарски:"""

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                self._generate_text, 
                                 prompt
            )
            
            if result:
                return self._extract_styled_response(result, text, "рыцарски")
            else:
                return text + " Честь и доблесть!"
                
        except Exception as e:
            logger.error(f"❌ Ошибка рыцарской трансформации: {e}")
            return text + " Честь и доблесть!"
    
    async def transform_to_robot(self, text: str) -> Optional[str]:
        """Трансформация в робот стиль"""
        if not self.initialized:
            return f"СИСТЕМА: {text.upper()}. КОНЕЦ ПЕРЕДАЧИ."
        
        try:
            prompt = f"""Переведи человеческую речь в речь робота:

Человек: Привет, как дела?
Робот: ПРИВЕТСТВИЕ ПОЛУЧЕНО. СТАТУС СИСТЕМ: ОПТИМАЛЬНЫЙ. ГОТОВ К ВЫПОЛНЕНИЮ КОМАНД.

Человек: Пойдем поедим
Робот: ИНИЦИИРУЮ ПРОТОКОЛ ПИТАНИЯ. НАПРАВЛЯЮСЬ К ПУНКТУ ПОЛУЧЕНИЯ ЭНЕРГИИ.

Человек: {text}
Робот:"""

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                self._generate_text, 
                prompt
            )
            
            if result:
                return self._extract_styled_response(result, text, "робот")
            else:
                return f"СИСТЕМА: {text.upper()}. КОНЕЦ ПЕРЕДАЧИ."
                
        except Exception as e:
            logger.error(f"❌ Ошибка роботской трансформации: {e}")
            return f"СИСТЕМА: {text.upper()}. КОНЕЦ ПЕРЕДАЧИ."
    
    def _create_pirate_prompt(self, text: str) -> str:
        """Создает промпт для пиратской трансформации"""
        return f"""Переведи обычную речь в пиратскую речь:

Обычно: Привет, как дела?
Пиратски: Аррр, приветствую, морской волк! Как поживаешь, старый корсар?

Обычно: Пойдем поедим
Пиратски: Поднимаем паруса к кормовой каюте за корабельным пайком, аррр!

Обычно: Работаю над проектом
Пиратски: Несу вахту над важным делом, тысяча чертей!

Обычно: {text}
Пиратски:"""
    
    def _generate_text(self, prompt: str) -> Optional[str]:
        """Генерирует текст с помощью модели"""
        try:
            results = self.pipeline(
                prompt,
                max_new_tokens=50,
                num_return_sequences=1,
                temperature=0.8,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            if results and len(results) > 0:
                generated = results[0]['generated_text'].strip()
                return generated
            return None
            
        except Exception as e:
            logger.error(f"❌ Ошибка генерации: {e}")
            return None
    
    def _extract_pirate_response(self, generated_text: str, original_text: str) -> str:
        """Извлекает пиратскую часть из сгенерированного текста"""
        try:
            # Ищем ответ после "Пиратски:"
            if "Пиратски:" in generated_text:
                pirate_part = generated_text.split("Пиратски:")[-1].strip()
                # Убираем лишние переносы строк и берем первую строку
                pirate_part = pirate_part.split('\n')[0].strip()
                
                if pirate_part and len(pirate_part) > 5:
                    return pirate_part
            
            # Fallback
            return self._fallback_pirate_transform(original_text)
            
        except Exception as e:
            logger.error(f"❌ Ошибка извлечения ответа: {e}")
            return self._fallback_pirate_transform(original_text)
    
    def _extract_styled_response(self, generated_text: str, original_text: str, style_marker: str) -> str:
        """Извлекает стилизованную часть из сгенерированного текста"""
        try:
            # Ищем ответ после маркера стиля
            if f"{style_marker}:" in generated_text.lower():
                styled_part = generated_text.lower().split(f"{style_marker}:")[-1].strip()
                styled_part = styled_part.split('\n')[0].strip()
                
                if styled_part and len(styled_part) > 5:
                    return styled_part
            
            return original_text
            
        except Exception as e:
            logger.error(f"❌ Ошибка извлечения стилизованного ответа: {e}")
            return original_text
    
    def _fallback_pirate_transform(self, text: str) -> str:
        """Fallback пиратская трансформация на случай сбоя модели"""
        import random
        
        pirate_endings = [
            " Аррр, морские волки!",
            " Поднять черный флаг!",
            " Тысяча чертей!",
            " Йо-хо-хо!",
            " Полундра, матросы!"
        ]
        
        return text + random.choice(pirate_endings)
    
    def get_model_status(self) -> dict:
        """Возвращает статус модели"""
        return {
            "initialized": self.initialized,
            "model_path": self.model_path,
            "model_exists": os.path.exists(self.model_path) if self.model_path else False,
            "torch_available": torch.cuda.is_available(),
            "device": "cuda" if torch.cuda.is_available() else "cpu"
        }

# Глобальный экземпляр сервиса
llm_transformer = LLMTextTransformer()
