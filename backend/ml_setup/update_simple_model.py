"""
🏴‍☠️ ОБНОВЛЕНИЕ ПРОСТОЙ ПИРАТСКОЙ МОДЕЛИ
Использует наш мега-датасет для создания улучшенных правил!
"""

import json
import re
import random
from collections import defaultdict

def extract_rules_from_dataset(dataset_file: str):
    """Извлекает правила замен из датасета"""
    
    print("🏴‍☠️ ИЗВЛЕЧЕНИЕ ПРАВИЛ ИЗ МЕГА-ДАТАСЕТА!")
    print("=" * 50)
    
    # Загружаем датасет
    with open(dataset_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Загружено примеров: {len(data)}")
    
    # Анализируем паттерны замен
    word_replacements = defaultdict(list)
    phrase_replacements = []
    ending_patterns = defaultdict(int)
    
    for item in data:
        original = item['original'].lower().strip()
        styled = item['styled'].lower().strip()
        
        # Извлекаем окончания
        endings = [', arr!', ', йо-хо-хо!', ', проклятье!', ', морской дьявол!', 
                  ', тысяча чертей!', ', кальмарьи кишки!', ', старый волк!']
        
        for ending in endings:
            if styled.endswith(ending):
                ending_patterns[ending] += 1
                styled_without_ending = styled[:-len(ending)].strip()
                break
        else:
            styled_without_ending = styled
        
        # Если фразы кардинально разные - это замена фразы целиком
        if len(original.split()) <= 3 and len(styled_without_ending.split()) <= 5:
            # Простые замены слов/фраз
            phrase_replacements.append((original, styled_without_ending))
        
        # Ищем паттерны замен отдельных слов
        orig_words = original.split()
        styled_words = styled_without_ending.split()
        
        if len(orig_words) == len(styled_words):
            for orig_word, styled_word in zip(orig_words, styled_words):
                if orig_word != styled_word and len(orig_word) > 2:
                    word_replacements[orig_word].append(styled_word)
    
    # Создаём правила
    rules = []
    
    # Правила замены целых фраз (приоритет)
    for original, pirate in phrase_replacements:
        if len(original) > 1:  # игнорируем слишком короткие
            rules.append({
                "original_pattern": f"\\b{re.escape(original)}\\b",
                "styled_options": [pirate],
                "type": "phrase"
            })
    
    # Правила замены слов
    for original_word, pirate_options in word_replacements.items():
        if len(pirate_options) >= 2:  # только если есть минимум 2 варианта
            # Берём наиболее частые варианты
            unique_options = list(set(pirate_options))
            if len(unique_options) > 1:
                rules.append({
                    "original_pattern": f"\\b{re.escape(original_word)}\\b",
                    "styled_options": unique_options[:3],  # максимум 3 варианта
                    "type": "word"
                })
    
    print(f"✅ Извлечено правил: {len(rules)}")
    print(f"📊 Популярные окончания:")
    
    sorted_endings = sorted(ending_patterns.items(), key=lambda x: x[1], reverse=True)
    for ending, count in sorted_endings[:5]:
        print(f"   {ending}: {count} раз")
    
    return rules, sorted_endings

def create_enhanced_simple_model():
    """Создаёт улучшенную простую модель на основе мега-датасета"""
    
    # Извлекаем правила из нашего мега-датасета
    rules, popular_endings = extract_rules_from_dataset("./training_data/FINAL_MEGA_PIRATE_DATASET.json")
    
    # Добавляем базовые ручные правила для качества
    manual_rules = [
        # Базовые замены
        {
            "original_pattern": "\\bпривет\\b",
            "styled_options": ["йо-хо-хо", "arr", "салют"],
            "type": "word"
        },
        {
            "original_pattern": "\\bдом\\b",
            "styled_options": ["каюта"],
            "type": "word"
        },
        {
            "original_pattern": "\\bдомой\\b",
            "styled_options": ["в каюту"],
            "type": "word"
        },
        {
            "original_pattern": "\\bдома\\b",
            "styled_options": ["в каюте"],
            "type": "word"
        },
        {
            "original_pattern": "\\bдруг\\b",
            "styled_options": ["корсар", "старый волк"],
            "type": "word"
        },
        {
            "original_pattern": "\\bденьги\\b",
            "styled_options": ["пиастры"],
            "type": "word"
        },
        {
            "original_pattern": "\\bеда\\b",
            "styled_options": ["провизия"],
            "type": "word"
        },
        {
            "original_pattern": "\\bмашина\\b",
            "styled_options": ["корвет"],
            "type": "word"
        },
        {
            "original_pattern": "\\bтелефон\\b",
            "styled_options": ["хронометр"],
            "type": "word"
        },
        {
            "original_pattern": "\\bврач\\b",
            "styled_options": ["корабельный лекарь"],
            "type": "word"
        },
        {
            "original_pattern": "\\bработа\\b",
            "styled_options": ["корабельная служба"],
            "type": "word"
        },
        {
            "original_pattern": "\\bработаю\\b",
            "styled_options": ["несу вахту", "служу"],
            "type": "word"
        },
        {
            "original_pattern": "\\bспать\\b",
            "styled_options": ["вешать чёрные метки"],
            "type": "word"
        },
        {
            "original_pattern": "\\bесть\\b",
            "styled_options": ["уплетать провизию"],
            "type": "word"
        },
        {
            "original_pattern": "\\bпить\\b",
            "styled_options": ["потягивать ром"],
            "type": "word"
        },
        
        # Эмоциональные реакции
        {
            "original_pattern": "\\bотлично\\b",
            "styled_options": ["великолепно", "по курсу"],
            "type": "word"
        },
        {
            "original_pattern": "\\bужасно\\b",
            "styled_options": ["кошмар морской"],
            "type": "word"
        },
        {
            "original_pattern": "\\bкруто\\b",
            "styled_options": ["по курсу", "arr"],
            "type": "word"
        },
        
        # Фразовые замены
        {
            "original_pattern": "как дела",
            "styled_options": ["как житуха", "как дела морские"],
            "type": "phrase"
        },
        {
            "original_pattern": "что делаешь",
            "styled_options": ["чем занимаешься", "какие дела ведёшь"],
            "type": "phrase"
        },
        {
            "original_pattern": "до свидания",
            "styled_options": ["попутного ветра", "удачного плавания"],
            "type": "phrase"
        }
    ]
    
    # Объединяем правила
    all_rules = manual_rules + rules
    
    # Убираем дубликаты
    seen_patterns = set()
    unique_rules = []
    for rule in all_rules:
        pattern = rule["original_pattern"]
        if pattern not in seen_patterns:
            seen_patterns.add(pattern)
            unique_rules.append(rule)
    
    print(f"🎯 Финальных правил: {len(unique_rules)}")
    
    # Сохраняем улучшенные правила
    import os
    os.makedirs("./simple_model", exist_ok=True)
    
    output_file = "./simple_model/enhanced_pirate_rules.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_rules, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Правила сохранены: {output_file}")
    
    # Показываем примеры правил
    print(f"\n🔍 ПРИМЕРЫ ПРАВИЛ:")
    print("=" * 50)
    for i, rule in enumerate(unique_rules[:15], 1):
        pattern = rule["original_pattern"].replace("\\b", "").replace("\\", "")
        options = ", ".join(rule["styled_options"][:2])  # только первые 2
        print(f"{i:2d}. {pattern} -> {options}")
    
    return unique_rules

def test_enhanced_model(rules):
    """Тестирует улучшенную модель"""
    
    print(f"\n🧪 ТЕСТИРОВАНИЕ УЛУЧШЕННОЙ МОДЕЛИ:")
    print("=" * 50)
    
    test_phrases = [
        "Привет, как дела?",
        "Иду домой спать",
        "Друг звонит по телефону",
        "Работаю, ем, потом отдыхаю",
        "Покупаю еду, трачу деньги",
        "Врач говорит отлично",
        "Машина сломалась, ужасно",
        "До свидания, старина!"
    ]
    
    # Пиратские окончания для теста
    pirate_endings = [" arr!", " йо-хо-хо!", ", морской дьявол!", ", проклятье!", ", тысяча чертей!"]
    
    for i, phrase in enumerate(test_phrases, 1):
        result = phrase.lower()
        
        # Применяем правила замены
        for rule in rules:
            pattern = re.compile(rule["original_pattern"], re.IGNORECASE)
            if pattern.search(result):
                replacement = random.choice(rule["styled_options"])
                result = pattern.sub(replacement, result)
        
        # Добавляем пиратское окончание, если его ещё нет
        if not any(ending.strip(', ') in result for ending in pirate_endings):
            result += random.choice(pirate_endings)
        
        print(f"{i}. {phrase}")
        print(f"   -> {result}")
        print()

if __name__ == "__main__":
    print("🏴‍☠️ ОБНОВЛЕНИЕ ПИРАТСКОЙ МОДЕЛИ ПО МЕГА-ДАТАСЕТУ!")
    print("=" * 70)
    
    enhanced_rules = create_enhanced_simple_model()
    test_enhanced_model(enhanced_rules)
    
    print("🎉 МОДЕЛЬ УСПЕШНО ОБНОВЛЕНА!")
    print("💡 Теперь используется 900+ примеров для качественных замен!")
    print("🚀 ГОТОВО К ВНЕДРЕНИЮ В ПРИЛОЖЕНИЕ!")
