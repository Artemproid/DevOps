"""
🏴‍☠️ ПАРСЕР ПИРАТСКОГО СЛОВАРЯ 

Превращаем найденный пиратский словарь в мощные тренировочные данные!
"""

import re
import json
import random
from typing import List, Tuple, Dict

def parse_pirate_dictionary(file_path: str) -> Dict[str, List[Tuple[str, str]]]:
    """Парсит пиратский словарь из файла"""
    
    print("🏴‍☠️ Парсим пиратский словарь...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Категории данных
    actions = []  # ДЕЙСТВИЯ: спать -> вешать чёрные метки
    comparisons = []  # СРАВНЕНИЯ: как попугай Флинта -> хитрый
    things = []  # ПРЕДМЕТЫ: каюта -> комната
    exclamations = []  # ВОСКЛИЦАНИЯ: Тысяча чертей!
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('|'):
            continue
            
        # Убираем номера строк
        line = re.sub(r'^\s*\d+\|', '', line)
        
        # Ищем паттерны
        if ' - ' in line:
            parts = line.split(' - ', 1)
            if len(parts) == 2:
                pirate_term = parts[0].strip().upper()
                normal_term = parts[1].strip()
                
                # Убираем точки с запятой
                normal_term = normal_term.rstrip(';')
                
                # Классифицируем
                if pirate_term.startswith('КАК '):
                    # Сравнения: КАК МОРСКОЙ ЧЕРТ - хитрый
                    comparisons.append((pirate_term, normal_term))
                elif any(verb in pirate_term for verb in ['ВЕШАТЬ', 'ДАТЬ', 'МЕРЯТЬСЯ', 'МЕТАТЬ', 'МУТИТЬ', 'НАБИВАТЬ', 'НАПРАВЛЯТЬ', 'ОТПРАВИТЬ', 'ПАЛИТЬ', 'ПОДНЯТЬ', 'ПРОМОЧИТЬ', 'ПРОСАЛИВАТЬ', 'СОЙТИСЬ', 'СНЯТЬСЯ', 'ТРЯСТИ']):
                    # Действия
                    actions.append((normal_term, pirate_term))
                else:
                    # Предметы и прочее
                    things.append((normal_term, pirate_term))
        
        elif line.endswith('!'):
            # Восклицания
            if not any(word in line.lower() for word in ['способ', 'судно', 'корабль', 'группа']):
                exclamations.append(line)
    
    print(f"📊 Найдено:")
    print(f"   🎬 Действий: {len(actions)}")
    print(f"   🆚 Сравнений: {len(comparisons)}")
    print(f"   📦 Предметов: {len(things)}")
    print(f"   💥 Восклицаний: {len(exclamations)}")
    
    return {
        'actions': actions,
        'comparisons': comparisons,
        'things': things,
        'exclamations': exclamations
    }

def generate_realistic_examples(pirate_data: Dict) -> List[Tuple[str, str]]:
    """Генерирует реалистичные примеры на основе словаря"""
    
    examples = []
    
    # ДЕЙСТВИЯ - создаём естественные предложения
    for normal, pirate in pirate_data['actions']:
        # Базовые примеры
        examples.append((f"Иду {normal}", f"Иду {pirate.lower()}, arr!"))
        examples.append((f"Пора {normal}", f"Пора {pirate.lower()}, йо-хо-хо!"))
        examples.append((f"Хочу {normal}", f"Хочу {pirate.lower()}, старый волк!"))
        
        # Более сложные
        if normal in ['есть', 'пить']:
            examples.append((f"Очень хочется {normal}", f"Пора {pirate.lower()}, проклятье!"))
        elif normal in ['спать', 'танцевать']:
            examples.append((f"Пойду {normal}", f"Пойду {pirate.lower()}, морской дьявол!"))
        elif normal in ['драться', 'ругаться']:
            examples.append((f"Готов {normal}", f"Готов {pirate.lower()}, arr!"))
    
    # СРАВНЕНИЯ - делаем описания людей
    for pirate_comp, normal_adj in pirate_data['comparisons']:
        adjective = normal_adj.split(',')[0].strip()  # берём первое прилагательное
        
        # Простые описания
        examples.append((f"Он очень {adjective}", f"Он {pirate_comp.lower()}, arr!"))
        examples.append((f"Она такая {adjective}", f"Она {pirate_comp.lower()}, йо-хо-хо!"))
        examples.append((f"Этот парень {adjective}", f"Этот парень {pirate_comp.lower()}, старый волк!"))
        
        # В диалогах
        examples.append((f"Какой {adjective}!", f"{pirate_comp}, проклятье!"))
    
    # ПРЕДМЕТЫ - заменяем в контексте
    for normal, pirate in pirate_data['things']:
        if normal in ['комната', 'кухня', 'повар', 'товарищ', 'часы', 'деньги']:
            # Простые замены
            examples.append((f"Где моя {normal}?", f"Где моя {pirate.lower()}, arr?"))
            examples.append((f"Иду в {normal}", f"Иду в {pirate.lower()}, йо-хо-хо!"))
            examples.append((f"Нужны {normal}", f"Нужны {pirate.lower()}, морской дьявол!"))
            
            # С артиклями
            if normal in ['повар', 'товарищ']:
                examples.append((f"Мой {normal} ушёл", f"Мой {pirate.lower()} сбежал, проклятье!"))
            elif normal in ['комната', 'кухня']:
                examples.append((f"Убираю {normal}", f"Убираю {pirate.lower()}, arr!"))
    
    # ВОСКЛИЦАНИЯ - добавляем к фразам
    for exclamation in pirate_data['exclamations']:
        if len(exclamation) < 50:  # только короткие
            # Реакции на события
            examples.append(("Вот дерьмо!", f"{exclamation}"))
            examples.append(("Чёрт побери!", f"{exclamation}"))
            examples.append(("Какого дьявола?", f"{exclamation}"))
            examples.append(("Проклятье!", f"{exclamation}"))
    
    # ДОПОЛНИТЕЛЬНЫЕ ШАБЛОНЫ
    base_phrases = [
        "Привет, как дела?",
        "Что происходит?", 
        "Иду домой",
        "Хорошая погода",
        "Плохое настроение",
        "Много работы",
        "Мало времени",
        "Вкусная еда",
        "Дорогие вещи",
        "Старые друзья"
    ]
    
    pirate_endings = [" arr!", " йо-хо-хо!", ", старый морской волк!", ", проклятье!", ", морской дьявол!"]
    
    for phrase in base_phrases:
        pirate_phrase = phrase + random.choice(pirate_endings)
        examples.append((phrase, pirate_phrase))
    
    return examples

def create_contextual_examples(pirate_data: Dict) -> List[Tuple[str, str]]:
    """Создаёт примеры в контексте диалогов"""
    
    examples = []
    
    # ДИАЛОГИ
    conversations = [
        # Приветствие
        ("Привет, старина!", "Йо-хо-хо, старый пройдоха!"),
        ("Как поживаешь?", "Как житуха, морской волк?"),
        ("Рад тебя видеть", "Рад видеть, arr!"),
        
        # Планы
        ("Что будешь делать сегодня?", "Что планируешь, старый пройдоха?"),
        ("Иду в магазин за продуктами", "Направляю корвет за провизией, arr!"),
        ("Хочу поспать немного", "Хочу вешать чёрные метки, йо-хо-хо!"),
        
        # Проблемы
        ("У меня проблемы с деньгами", "У меня беда с пиастрами, проклятье!"),
        ("Потерял ключи от дома", "Потерял ключи от каюты, морской дьявол!"),
        ("Сломался телефон", "Накрылся хронометр медным тазом!"),
        
        # Эмоции
        ("Я очень злой сегодня", "Я побратался с морским дьяволом, arr!"),
        ("Хорошее настроение", "Поднял Весёлого Роджера, йо-хо-хо!"),
        ("Устал как собака", "Устал как после абордажа, проклятье!"),
        
        # События
        ("Вчера была драка в баре", "Вчера сходились якорями в таверне!"),
        ("Покупал новую одежду", "Бренчал золотишком за новое обмундирование!"),
        ("Ходил к врачу", "Навещал корабельного лекаря, arr!"),
        
        # Прощание
        ("До встречи!", "Попутного ветра, старый волк!"),
        ("Удачи в делах", "Попутного ветра в делах, arr!"),
        ("Увидимся завтра", "Встретимся на следующих склянках!")
    ]
    
    examples.extend(conversations)
    
    return examples

def enhance_pirate_training_data():
    """Создаёт улучшенные тренировочные данные на основе словаря"""
    
    print("🏴‍☠️ УЛУЧШАЕМ ПИРАТСКИЕ ДАННЫЕ!")
    print("=" * 50)
    
    # Парсим словарь
    pirate_data = parse_pirate_dictionary("../../pirates.txt")
    
    # Генерируем примеры
    print("\n🎯 Генерируем примеры...")
    realistic_examples = generate_realistic_examples(pirate_data)
    contextual_examples = create_contextual_examples(pirate_data)
    
    # Объединяем все примеры
    all_examples = realistic_examples + contextual_examples
    
    # Убираем дубликаты
    unique_examples = list(set(all_examples))
    
    print(f"📊 Статистика:")
    print(f"   🎬 Реалистичных примеров: {len(realistic_examples)}")
    print(f"   💬 Контекстных примеров: {len(contextual_examples)}")
    print(f"   ✨ Уникальных примеров: {len(unique_examples)}")
    
    # Форматируем для обучения
    formatted_data = []
    for normal, pirate in unique_examples:
        formatted_data.append({
            "text": f"Стиль пират: {normal} -> {pirate}",
            "style": "пират",
            "original": normal,
            "styled": pirate
        })
    
    # Перемешиваем
    random.shuffle(formatted_data)
    
    # Сохраняем
    import os
    os.makedirs("./training_data", exist_ok=True)
    
    output_file = "./training_data/enhanced_pirate_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Сохранено в: {output_file}")
    
    # Показываем примеры
    print(f"\n🎲 СЛУЧАЙНЫЕ ПРИМЕРЫ:")
    print("=" * 50)
    for i, example in enumerate(random.sample(formatted_data, min(10, len(formatted_data)))):
        print(f"{i+1:2d}. {example['original']} -> {example['styled']}")
    
    return formatted_data

if __name__ == "__main__":
    print("🏴‍☠️ ОПЕРАЦИЯ 'МОРСКОЙ РАЗБОЙ ДАННЫХ'")
    print("=" * 50)
    
    enhanced_data = enhance_pirate_training_data()
    
    print(f"\n🎉 УСПЕХ! Создано {len(enhanced_data)} примеров!")
    print("📋 Теперь у нас есть МЕГА-БАЗА для обучения пиратской модели!")
    print("\n💡 ЧТО ДАЛЬШЕ:")
    print("   1. Запустить обучение модели")
    print("   2. Тестировать результаты") 
    print("   3. Радоваться как пираты! 🏴‍☠️")
