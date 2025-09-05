"""
🏴‍☠️ ПРОСТАЯ ПИРАТСКАЯ МОДЕЛЬ БЕЗ PYTORCH

Создаём простую модель на основе шаблонов и правил
Без сложного машинного обучения
"""

import json
import random
import re
from typing import Dict, List, Tuple

class SimplePirateModel:
    """Простая модель стилизации на основе правил и шаблонов"""
    
    def __init__(self):
        self.rules = {}
        self.exclamations = []
        self.pirate_endings = [" arr!", " йо-хо-хо!", ", старый морской волк!", ", проклятье!", ", морской дьявол!"]
        
    def load_training_data(self, data_path):
        """Загружает тренировочные данные и создаёт правила"""
        
        print("📚 Загружаем данные и создаём правила...")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Анализируем примеры и создаём правила
        for item in data:
            original = item['original'].lower()
            styled = item['styled']
            
            # Ищем паттерны замен
            if ' -> ' in item['text']:
                parts = item['text'].split(' -> ')
                if len(parts) == 2:
                    clean_original = parts[0].replace('Стиль пират: ', '').strip().lower()
                    clean_styled = parts[1].strip()
                    
                    # Сохраняем правила замены
                    self.rules[clean_original] = clean_styled
        
        # Добавляем восклицания
        self.exclamations = [
            "Тысяча чертей!",
            "Разрази меня гром!",
            "Кальмарьи кишки!",
            "Карамба!",
            "Проклятье медузы!",
            "Йо-хо-хо!",
            "Arr!"
        ]
        
        print(f"✅ Создано {len(self.rules)} правил замены")
        
    def piratify_text(self, text: str) -> str:
        """Превращает обычный текст в пиратский"""
        
        text = text.strip().lower()
        
        # Прямые замены из правил
        if text in self.rules:
            return self.rules[text]
        
        # Ищем частичные совпадения
        for rule_text, pirate_text in self.rules.items():
            if self._is_similar(text, rule_text):
                return pirate_text
        
        # Базовые правила замещения
        pirate_text = self._apply_basic_rules(text)
        
        # Добавляем пиратское окончание
        if not any(ending.strip(' .,!?') in pirate_text for ending in self.pirate_endings):
            ending = random.choice(self.pirate_endings)
            pirate_text += ending
        
        return pirate_text
    
    def _is_similar(self, text1: str, text2: str) -> bool:
        """Проверяет похожесть текстов"""
        
        # Убираем знаки препинания
        text1 = re.sub(r'[^\w\s]', '', text1)
        text2 = re.sub(r'[^\w\s]', '', text2)
        
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        # Если есть общие слова
        common_words = words1.intersection(words2)
        if common_words and len(common_words) >= len(words1) * 0.5:
            return True
        
        return False
    
    def _apply_basic_rules(self, text: str) -> str:
        """Применяет базовые правила стилизации"""
        
        # Словарь базовых замен
        replacements = {
            'привет': 'йо-хо-хо',
            'как дела': 'как житуха',
            'спать': 'вешать чёрные метки',
            'есть': 'набивать трюм',
            'пить': 'промочить горло',
            'идти': 'направлять корвет',
            'деньги': 'пиастры',
            'золото': 'золотишко',
            'комната': 'каюта',
            'кухня': 'камбуз',
            'повар': 'кок',
            'друг': 'старый пройдоха',
            'товарищ': 'старый волк',
            'часы': 'хронометр',
            'туалет': 'гальюн',
            'покупать': 'бренчать золотишком',
            'драться': 'сойтись якорями',
            'танцевать': 'трясти костями',
            'ругаться': 'палить из всех пушек',
            'умереть': 'отправиться кормить рыб',
            'убить': 'отправить на дно',
            'сдаться': 'поднять белый флаг',
            'уйти': 'сняться с якоря',
            'веселиться': 'поднять весёлого роджера',
            'злиться': 'побрататься с морским дьяволом'
        }
        
        result = text
        
        # Применяем замены
        for old_word, new_word in replacements.items():
            if old_word in result:
                result = result.replace(old_word, new_word)
        
        # Добавляем пиратские прилагательные
        if 'хитрый' in result:
            result = result.replace('хитрый', 'как морской чёрт')
        elif 'умный' in result:
            result = result.replace('умный', 'как морская грамота')
        elif 'богатый' in result:
            result = result.replace('богатый', 'как губернатор ямайки')
        elif 'быстрый' in result:
            result = result.replace('быстрый', 'как одноногий сильвер')
        
        return result
    
    def test_model(self):
        """Тестирует модель на примерах"""
        
        print("\n🧪 ТЕСТИРУЕМ ПРОСТУЮ ПИРАТСКУЮ МОДЕЛЬ:")
        print("=" * 60)
        
        test_phrases = [
            "Привет, как дела?",
            "Иду спать",
            "Хочу есть",
            "Потерял ключи",
            "Нужны деньги",
            "Где туалет?",
            "Иду в магазин",
            "Он очень хитрый",
            "Готовлю обед",
            "До свидания"
        ]
        
        for phrase in test_phrases:
            pirate_phrase = self.piratify_text(phrase)
            print(f"   '{phrase}' -> '{pirate_phrase}'")

def create_simple_pirate_service():
    """Создаёт и сохраняет простую пиратскую модель"""
    
    print("🏴‍☠️ СОЗДАЁМ ПРОСТУЮ ПИРАТСКУЮ МОДЕЛЬ!")
    print("=" * 60)
    
    # Создаём модель
    model = SimplePirateModel()
    
    # Загружаем данные
    try:
        model.load_training_data("./training_data/enhanced_pirate_data.json")
    except FileNotFoundError:
        print("❌ Файл с данными не найден, используем базовые правила")
    
    # Тестируем
    model.test_model()
    
    # Сохраняем модель в виде JSON правил
    model_data = {
        'rules': model.rules,
        'exclamations': model.exclamations,
        'pirate_endings': model.pirate_endings
    }
    
    import os
    os.makedirs("./simple_model", exist_ok=True)
    
    with open("./simple_model/pirate_rules.json", 'w', encoding='utf-8') as f:
        json.dump(model_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Простая модель сохранена в: ./simple_model/pirate_rules.json")
    
    return model

if __name__ == "__main__":
    print("🏴‍☠️ ОПЕРАЦИЯ 'ПРОСТОЙ МОРСКОЙ РАЗБОЙ'")
    print("=" * 50)
    
    print("\n💡 ОБЪЯСНЕНИЕ:")
    print("   Создаём простую модель БЕЗ сложного машинного обучения")
    print("   Используем правила и шаблоны из твоего словаря")
    print("   Работает быстро и не требует мощного железа!")
    
    # Создаём модель
    model = create_simple_pirate_service()
    
    # Интерактивный тест
    print(f"\n🎮 ИНТЕРАКТИВНЫЙ ТЕСТ:")
    print("   Введи фразу, а я переведу её на пиратский!")
    print("   (Введи 'quit' для выхода)")
    
    while True:
        user_input = input(f"\n> ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'выход', 'стоп']:
            print("🏴‍☠️ Попутного ветра, старый волк!")
            break
        
        if user_input:
            pirate_result = model.piratify_text(user_input)
            print(f"🏴‍☠️ {pirate_result}")
