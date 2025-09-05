"""
Smart Transformer - Умный трансформатор без тяжелых зависимостей
Симулирует работу LLM но работает на правилах
"""

import os
import logging
import random
from typing import Optional, Dict, List
import asyncio

logger = logging.getLogger(__name__)

class SmartTextTransformer:
    """
    Умный трансформатор текста без ML зависимостей
    Использует продвинутые правила для имитации LLM
    """
    
    def __init__(self):
        self.initialized = True
        self.style_rules = self._load_style_rules()
        logger.info("🧠 Smart Transformer инициализирован (без ML зависимостей)")
    
    def _load_style_rules(self) -> Dict:
        """Загружает продвинутые правила трансформации"""
        return {
            "pirate": {
                "word_replacements": {
                    # Обращения
                    "друг": ["корсар", "старый волк", "морской волк"],
                    "друзья": ["команда", "экипаж", "братва"],
                    "человек": ["морской волк", "корсар", "матрос"],
                    "люди": ["команда", "экипаж", "морские волки"],
                    "парень": ["юнга", "корсар"],
                    "девушка": ["морская дева", "русалка"],
                    
                    # Места
                    "дом": ["корабль", "каюта", "судно"],
                    "комната": ["каюта", "кубрик"],
                    "кухня": ["камбуз"],
                    "туалет": ["гальюн"],
                    "дорога": ["морской путь", "курс"],
                    "город": ["порт", "гавань"],
                    
                    # Действия
                    "идти": ["плыть", "держать курс", "поднять паруса"],
                    "бежать": ["мчаться под всеми парусами"],
                    "работать": ["нести вахту", "служить на корабле"],
                    "спать": ["отдыхать в каюте", "спать в койке"],
                    "есть": ["употреблять корабельный паек"],
                    "пить": ["пить ром", "осушать кружку"],
                    
                    # Предметы
                    "деньги": ["пиастры", "золото", "сокровища"],
                    "еда": ["корабельный паек", "галеты", "солонина"],
                    "вода": ["пресная вода", "ром"],
                    "оружие": ["абордажная сабля", "мушкет"],
                    "машина": ["корабль", "судно"],
                    
                    # Эмоции
                    "хорошо": ["отлично как попутный ветер"],
                    "плохо": ["хуже штиля"],
                    "отлично": ["превосходно как золото"],
                    "ужасно": ["хуже кракена"]
                },
                "phrase_patterns": {
                    r"как дела\?": ["как поживаешь, морской волк?", "как дела в открытом море?"],
                    r"что происходит\?": ["что творится на палубе?", "какие новости с моря?"],
                    r"пойдем": ["поднимаем паруса", "держим курс на"],
                    r"давай": ["полный вперед", "все руки на палубу"],
                    r"помоги": ["протяни руку помощи", "подсоби товарищу"],
                    r"спасибо": ["благодарю, старый морской волк", "спасибо, корсар"]
                },
                "endings": [
                    "аррр!", "йо-хо-хо!", "тысяча чертей!", "кальмарьи кишки!",
                    "разрази меня гром!", "полундра!", "свистать всех наверх!",
                    "поднять черный флаг!", "все на абордаж!", "морские волки!",
                    "держи ветер в паруса!", "попутного ветра!", "семь футов под килем!"
                ],
                "prefixes": [
                    "Слушай сюда, корсар,", "Аррр, морской волк,", "Эй, старый пират,",
                    "Братва морская,", "Команда,", "Матросы,"
                ]
            },
            
            "knight": {
                "word_replacements": {
                    "друг": ["верный соратник", "благородный рыцарь"],
                    "враг": ["злодей", "нечестивец", "супостат"],
                    "дом": ["замок", "крепость", "обитель"],
                    "еда": ["пиршество", "трапеза"],
                    "идти": ["отправиться", "держать путь"],
                    "хорошо": ["превосходно", "благородно"],
                    "плохо": ["недостойно", "позорно"]
                },
                "endings": [
                    "честь и доблесть!", "во славу короля!", "за правое дело!",
                    "клянусь мечом!", "именем справедливости!", "да будет так!"
                ],
                "prefixes": [
                    "Милорд,", "Благородный рыцарь,", "Достойный воин,",
                    "О благородный,"
                ]
            },
            
            "robot": {
                "word_replacements": {
                    "привет": ["ПРИВЕТСТВИЕ ПОЛУЧЕНО"],
                    "пока": ["ЗАВЕРШЕНИЕ СЕАНСА СВЯЗИ"],
                    "да": ["УТВЕРДИТЕЛЬНО"],
                    "нет": ["ОТРИЦАТЕЛЬНО"],
                    "хорошо": ["СТАТУС: ОПТИМАЛЬНЫЙ"],
                    "плохо": ["ОШИБКА В СИСТЕМЕ"],
                    "понял": ["ДАННЫЕ ОБРАБОТАНЫ"],
                    "спасибо": ["БЛАГОДАРНОСТЬ ЗАРЕГИСТРИРОВАНА"]
                },
                "endings": [
                    "КОНЕЦ ПЕРЕДАЧИ.", "СИСТЕМА ГОТОВА.", "ПРОТОКОЛ ЗАВЕРШЕН.",
                    "МИССИЯ ВЫПОЛНЕНА.", "ДАННЫЕ ОБНОВЛЕНЫ.", "ГОТОВ К ВЫПОЛНЕНИЮ КОМАНД."
                ],
                "prefixes": [
                    "СИСТЕМА:", "ПРОТОКОЛ:", "УВЕДОМЛЕНИЕ:", "СТАТУС:",
                    "РОБОТ-АССИСТЕНТ:", "ИНИЦИИРУЮ:"
                ]
            }
        }
    
    async def transform_to_pirate(self, text: str) -> Optional[str]:
        """Трансформация в пиратский стиль"""
        return await self.transform_to_style(text, "pirate")
    
    async def transform_to_knight(self, text: str) -> Optional[str]:
        """Трансформация в рыцарский стиль"""
        return await self.transform_to_style(text, "knight")
    
    async def transform_to_robot(self, text: str) -> Optional[str]:
        """Трансформация в робот стиль"""
        return await self.transform_to_style(text, "robot")
    
    async def transform_to_style(self, text: str, style: str) -> str:
        """Универсальная трансформация"""
        if style not in self.style_rules:
            return text
        
        # Симулируем задержку как у настоящей LLM
        await asyncio.sleep(0.1)
        
        rules = self.style_rules[style]
        transformed = text.lower()
        changes_made = False
        
        # Применяем замены фраз (более высокий приоритет)
        if "phrase_patterns" in rules:
            import re
            for pattern, replacements in rules["phrase_patterns"].items():
                if re.search(pattern, transformed, re.IGNORECASE):
                    replacement = random.choice(replacements)
                    transformed = re.sub(pattern, replacement, transformed, flags=re.IGNORECASE)
                    changes_made = True
                    break
        
        # Применяем замены слов
        for original, replacements in rules["word_replacements"].items():
            if original.lower() in transformed:
                replacement = random.choice(replacements)
                # Заменяем целые слова
                import re
                pattern = r'\b' + re.escape(original.lower()) + r'\b'
                if re.search(pattern, transformed):
                    transformed = re.sub(pattern, replacement, transformed)
                    changes_made = True
        
        # Добавляем стилистические элементы
        if changes_made or random.random() < 0.7:  # 70% шанс добавить стиль даже без замен
            # Случайный префикс (30% шанс)
            if random.random() < 0.3 and "prefixes" in rules:
                prefix = random.choice(rules["prefixes"])
                transformed = f"{prefix} {transformed}"
            
            # Обязательное окончание
            ending = random.choice(rules["endings"])
            
            # Умное добавление окончания
            if transformed.endswith('.'):
                transformed = transformed[:-1] + f", {ending}"
            elif transformed.endswith('!') or transformed.endswith('?'):
                transformed = transformed + f" {ending}"
            else:
                transformed = transformed + f", {ending}"
        
        # Капитализация для роботов
        if style == "robot":
            transformed = transformed.upper()
        else:
            # Капитализируем первую букву
            transformed = transformed.capitalize()
        
        logger.info(f"🎭 Smart Transform [{style}]: '{text}' -> '{transformed}'")
        return transformed
    
    def get_model_status(self) -> dict:
        """Возвращает статус 'модели'"""
        return {
            "initialized": True,
            "model_type": "smart_rules_engine",
            "styles_available": list(self.style_rules.keys()),
            "torch_required": False,
            "fast_inference": True,
            "device": "cpu_optimized"
        }

# Глобальный экземпляр
smart_transformer = SmartTextTransformer()
