import json
import re
import os
import random
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class PirateTransformer:
    def __init__(self, rules_file_path="backend/ml_setup/simple_model/pirate_rules.json"):
        self.rules = self._load_rules(rules_file_path)
        logger.info(f"🏴‍☠️ Пиратская модель загружена: {len(self.rules)} правил")

    def _load_rules(self, file_path):
        try:
            # Adjust path for Docker environment - всегда используем /app путь в Docker
            docker_path = "/app/" + file_path
            if os.path.exists(docker_path):
                file_path = docker_path
            
            with open(file_path, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
            
            # Compile regex patterns
            compiled_rules = []
            for rule in rules_data:
                compiled_rules.append({
                    "original_pattern": re.compile(rule["original_pattern"], re.IGNORECASE),
                    "styled_options": rule["styled_options"],
                    "type": rule.get("type", "word")
                })
            return compiled_rules
        except FileNotFoundError:
            logger.error(f"❌ Файл правил не найден: {file_path}")
            return self._get_fallback_rules()
        except json.JSONDecodeError:
            logger.error(f"❌ Ошибка парсинга JSON в файле правил: {file_path}")
            return self._get_fallback_rules()
        except Exception as e:
            logger.error(f"❌ Неизвестная ошибка при загрузке правил: {e}")
            return self._get_fallback_rules()

    def _get_fallback_rules(self):
        """Возвращает базовые правила если файл не загрузился"""
        fallback_rules = [
            {
                "original_pattern": re.compile(r"\bпривет\b", re.IGNORECASE),
                "styled_options": ["йо-хо-хо", "arr"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bдом\b", re.IGNORECASE),
                "styled_options": ["каюта"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bдруг\b", re.IGNORECASE),
                "styled_options": ["корсар", "старый волк"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bденьги\b", re.IGNORECASE),
                "styled_options": ["пиастры"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bработаю\b", re.IGNORECASE),
                "styled_options": ["несу вахту"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bидти\b", re.IGNORECASE),
                "styled_options": ["плыть", "держать курс"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bидём\b", re.IGNORECASE),
                "styled_options": ["поднимаем паруса", "держим курс"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bеда\b", re.IGNORECASE),
                "styled_options": ["корабельный паек", "галеты"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bпить\b", re.IGNORECASE),
                "styled_options": ["пить ром"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bводу\b", re.IGNORECASE),
                "styled_options": ["морскую воду", "ром"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bчеловек\b", re.IGNORECASE),
                "styled_options": ["морской волк", "корсар"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bлюди\b", re.IGNORECASE),
                "styled_options": ["команда", "экипаж", "морские волки"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bспать\b", re.IGNORECASE),
                "styled_options": ["отдыхать в каюте"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bдорога\b", re.IGNORECASE),
                "styled_options": ["морской путь", "курс"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bстарый\b", re.IGNORECASE),
                "styled_options": ["бывалый", "морской волчара"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bбольшой\b", re.IGNORECASE),
                "styled_options": ["огромный как кит"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bплохо\b", re.IGNORECASE),
                "styled_options": ["хуже чёртовой бури"],
                "type": "word"
            },
            {
                "original_pattern": re.compile(r"\bхорошо\b", re.IGNORECASE),
                "styled_options": ["отлично как попутный ветер"],
                "type": "word"
            }
        ]
        return fallback_rules

    def transform(self, text: str) -> str:
        if not self.rules:
            return text + " (no pirate rules loaded, arr!)"
        
        transformed_text = text
        changes_made = False
        
        # Применяем правила фраз сначала (приоритет)
        for rule in self.rules:
            if rule["type"] == "phrase":
                if rule["original_pattern"].search(transformed_text):
                    transformed_text = rule["original_pattern"].sub(
                        random.choice(rule["styled_options"]), 
                        transformed_text
                    )
                    changes_made = True
        
        # Потом применяем правила слов
        for rule in self.rules:
            if rule["type"] == "word":
                if rule["original_pattern"].search(transformed_text):
                    transformed_text = rule["original_pattern"].sub(
                        random.choice(rule["styled_options"]), 
                        transformed_text
                    )
                    changes_made = True
        
        # Если были изменения, добавляем пиратские восклицания
        if changes_made:
            pirate_exclamations = [
                "аррр!", "йо-хо-хо!", "морские волки!", "тысяча чертей!", 
                "разрази меня гром!", "кальмарьи кишки!", "проклятье!", 
                "старина!", "морской дьявол!"
            ]
            
            if not any(exc in transformed_text.lower() for exc in pirate_exclamations):
                if transformed_text.endswith('.'):
                    transformed_text = transformed_text[:-1] + f", {random.choice(pirate_exclamations)}"
                else:
                    transformed_text += f", {random.choice(pirate_exclamations)}"
        else:
            # Если замен не было, добавляем классические пиратские фразы
            pirate_additions = [
                "Аррр, матросы!",
                "Поднять черный флаг!",
                "Все на абордаж!",
                "Пятнадцать человек на сундук мертвеца!",
                "Полундра!",
                "Свистать всех наверх!",
                "Держи ветер в паруса!"
            ]
            
            transformed_text += f" {random.choice(pirate_additions)}"
        
        # Капитализируем первую букву
        return transformed_text.capitalize()
    
    async def transform_with_llm(self, text: str) -> str:
        """
        Трансформация с помощью Smart AI (быстро и без torch)
        """
        try:
            # Используем умный трансформер
            from app.services.smart_transformer import smart_transformer
            
            # Пробуем Smart AI трансформацию
            smart_result = await smart_transformer.transform_to_pirate(text)
            if smart_result and smart_result != text:
                logger.info(f"🧠 Использована Smart AI трансформация: '{text}' -> '{smart_result}'")
                return smart_result
                
        except Exception as e:
            logger.warning(f"⚠️ Smart AI недоступна, используем regex: {e}")
        
        # Fallback к обычной трансформации
        logger.info(f"🔄 Fallback к regex трансформации для: '{text}'")
        return self.transform(text)

pirate_transformer = PirateTransformer()