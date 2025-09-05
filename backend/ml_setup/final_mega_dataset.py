"""
🏴‍☠️ ФИНАЛЬНЫЙ МЕГА-ДАТАСЕТ СОЗДАТЕЛЬ
Объединяем ВСЕ датасеты в один ГИГАНТСКИЙ!
"""

import json
import random
import os
from typing import List, Dict

def load_existing_datasets() -> List[Dict]:
    """Загружает все существующие датасеты"""
    
    all_data = []
    dataset_files = [
        "./training_data/mega_pirate_dataset.json",
        "./training_data/super_pirate_dataset.json",
        "./training_data/enhanced_pirate_data.json"  # если есть
    ]
    
    for file_path in dataset_files:
        if os.path.exists(file_path):
            print(f"📁 Загружаем: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
                print(f"   ✅ Загружено: {len(data)} примеров")
        else:
            print(f"   ❌ Файл не найден: {file_path}")
    
    return all_data

def create_additional_examples() -> List[Dict]:
    """Создаёт дополнительные примеры для достижения 1000+"""
    
    additional_examples = []
    
    # Вопросительные предложения
    question_pairs = [
        ("Как дела?", "Как житуха, старый волк?"),
        ("Что делаешь?", "Чем занимаешься, морской дьявол?"),
        ("Где ты?", "Где твой корвет бросил якорь, arr?"),
        ("Когда встретимся?", "Когда корабли встретятся, проклятье?"),
        ("Почему опаздываешь?", "Почему тормозишь, кальмарьи кишки?"),
        ("Сколько это стоит?", "Сколько пиастров просят, тысяча чертей?"),
        ("Куда идёшь?", "Куда держишь курс, старина?"),
        ("Откуда ты?", "Откуда твой корвет, морской волк?"),
        ("Зачем это нужно?", "К чему это, йо-хо-хо?"),
        ("Кто это?", "Кто сей персонаж, разрази меня гром?"),
    ]
    
    # Отрицательные предложения
    negative_pairs = [
        ("Не хочу", "Не буду, проклятье!"),
        ("Не могу", "Не в силах, морской дьявол!"),
        ("Не знаю", "Понятия не имею, arr!"),
        ("Не помню", "Память изменяет, тысяча чертей!"),
        ("Не понимаю", "Темна вода во облацех, старина!"),
        ("Не слышу", "Уши заложило, кальмарьи кишки!"),
        ("Не вижу", "Глаза подводят, йо-хо-хо!"),
        ("Не верю", "Сомневаюсь, старый волк!"),
        ("Не согласен", "Против течения иду, морской дьявол!"),
        ("Не получается", "Не выходит, проклятье!"),
    ]
    
    # Восклицательные предложения
    exclamation_pairs = [
        ("Отлично!", "Великолепно, arr!"),
        ("Ужасно!", "Кошмар морской, тысяча чертей!"),
        ("Невероятно!", "Разрази меня гром!"),
        ("Прекрасно!", "Замечательно, старый волк!"),
        ("Ужас!", "Кальмарьи кишки, что творится!"),
        ("Классно!", "По курсу, морской дьявол!"),
        ("Супер!", "Йо-хо-хо, отлично!"),
        ("Кошмар!", "Морской дьявол, что за беда!"),
        ("Здорово!", "Попутный ветер, проклятье!"),
        ("Ерунда!", "Чушь собачья, старина!"),
    ]
    
    # Сложные предложения
    complex_pairs = [
        ("Если будет хорошая погода, пойдём гулять", "Если попутный ветер подует, отправимся в плавание, arr!"),
        ("Когда закончу работу, приду домой", "Когда вахту отстою, в каюту вернусь, проклятье!"),
        ("Пока ты занят, я подожду", "Пока ты в делах, подожду на якоре, морской дьявол!"),
        ("Хотя устал, продолжу работать", "Хоть силы на исходе, службу продолжу, тысяча чертей!"),
        ("Поскольку дождь, останусь дома", "Раз шторм, в каюте засяду, старый волк!"),
        ("После того как поем, пойду спать", "После провизии чёрные метки вешать пойду, йо-хо-хо!"),
        ("До того как уйти, приберу", "Прежде чем отчалить, порядок наведу, старина!"),
        ("В то время как ты спишь, я работаю", "Пока ты метки вешаешь, я вахту несу, кальмарьи кишки!"),
        ("Несмотря на усталость, помогу", "Невзирая на то что силы на исходе, подсоблю, arr!"),
        ("Чтобы не опоздать, выйду рано", "Дабы не тормозить, паруса рано подниму, морской дьявол!"),
    ]
    
    # Диалоговые цепочки
    dialogue_pairs = [
        ("Как дела? - Хорошо", "Как житуха, старый волк? - Отлично, arr!"),
        ("Что нового? - Ничего особенного", "Что нового в морях? - Штиль полный, проклятье!"),
        ("Пойдём есть? - Конечно", "Направимся в камбуз? - Само собой, морской дьявол!"),
        ("Устал? - Очень", "Силы на исходе? - Чертовски, тысяча чертей!"),
        ("Помощь нужна? - Да", "Подмога требуется? - Arr, старина!"),
        ("Время есть? - Немного", "Свободное время имеется? - Чуток, кальмарьи кишки!"),
        ("Понятно? - Да", "Ясно? - Как день, йо-хо-хо!"),
        ("Согласен? - Нет", "Поддерживаешь? - Ни за какие пиастры, старый волк!"),
        ("Готов? - Почти", "К отплытию готов? - Практически, морской дьявол!"),
        ("Идём? - Пошли", "Отчаливаем? - Поднимаем якорь, проклятье!"),
    ]
    
    # Объединяем все пары
    all_pairs = question_pairs + negative_pairs + exclamation_pairs + complex_pairs + dialogue_pairs
    
    # Форматируем в нужный формат
    for original, pirate in all_pairs:
        additional_examples.append({
            "text": f"Стиль пират: {original} -> {pirate}",
            "style": "пират",
            "original": original,
            "styled": pirate
        })
    
    # Генерируем вариации с временными маркерами
    time_markers = ["сегодня", "завтра", "вчера", "утром", "днём", "вечером", "ночью"]
    base_phrases = [
        ("работаю", "несу вахту"),
        ("отдыхаю", "предаюсь морской неге"),
        ("ем", "уплетаю провизию"),
        ("сплю", "вешаю чёрные метки"),
        ("гуляю", "брожу по палубе"),
        ("учусь", "постигаю морскую науку"),
        ("готовлю", "колдую в камбузе"),
        ("убираю", "навожу порядок"),
        ("читаю", "изучаю корабельные журналы"),
        ("смотрю телевизор", "наблюдаю театр теней"),
    ]
    
    for time_marker in time_markers:
        for normal_action, pirate_action in base_phrases:
            original = f"{time_marker} {normal_action}"
            pirate = f"{time_marker} {pirate_action}, arr!"
            
            additional_examples.append({
                "text": f"Стиль пират: {original} -> {pirate}",
                "style": "пират",
                "original": original,
                "styled": pirate
            })
    
    print(f"🔥 Создано дополнительных примеров: {len(additional_examples)}")
    return additional_examples

def create_final_mega_dataset():
    """Создаёт финальный мега-датасет"""
    
    print("🏴‍☠️ СОЗДАНИЕ ФИНАЛЬНОГО МЕГА-ДАТАСЕТА!")
    print("=" * 70)
    
    # Загружаем существующие данные
    print("\n📚 ЗАГРУЗКА СУЩЕСТВУЮЩИХ ДАТАСЕТОВ:")
    existing_data = load_existing_datasets()
    
    # Создаём дополнительные примеры
    print("\n🔥 СОЗДАНИЕ ДОПОЛНИТЕЛЬНЫХ ПРИМЕРОВ:")
    additional_data = create_additional_examples()
    
    # Объединяем всё
    all_data = existing_data + additional_data
    
    # Убираем дубликаты по полю 'original'
    print("\n🧹 УДАЛЕНИЕ ДУБЛИКАТОВ:")
    seen_originals = set()
    unique_data = []
    
    for item in all_data:
        original = item.get('original', '').lower().strip()
        if original not in seen_originals and original:
            seen_originals.add(original)
            unique_data.append(item)
    
    print(f"   🔍 Исходных примеров: {len(all_data)}")
    print(f"   ✨ Уникальных примеров: {len(unique_data)}")
    
    # Перемешиваем для лучшего обучения
    random.shuffle(unique_data)
    
    # Сохраняем финальный датасет
    os.makedirs("./training_data", exist_ok=True)
    output_file = "./training_data/FINAL_MEGA_PIRATE_DATASET.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 ФИНАЛЬНЫЙ ДАТАСЕТ СОХРАНЁН:")
    print(f"   📁 Файл: {output_file}")
    print(f"   📊 Размер: {len(unique_data)} примеров")
    
    # Статистика по типам
    categories = {}
    for item in unique_data:
        original = item['original'].lower()
        if '?' in original:
            categories['вопросы'] = categories.get('вопросы', 0) + 1
        elif '!' in original:
            categories['восклицания'] = categories.get('восклицания', 0) + 1
        elif original.startswith('не '):
            categories['отрицания'] = categories.get('отрицания', 0) + 1
        elif any(word in original for word in ['если', 'когда', 'пока', 'хотя']):
            categories['сложные'] = categories.get('сложные', 0) + 1
        else:
            categories['простые'] = categories.get('простые', 0) + 1
    
    print(f"\n📈 СТАТИСТИКА ПО ТИПАМ:")
    for category, count in categories.items():
        print(f"   {category.title()}: {count}")
    
    # Показываем лучшие примеры
    print(f"\n🎯 СЛУЧАЙНЫЕ ПРИМЕРЫ ИЗ ФИНАЛЬНОГО ДАТАСЕТА:")
    print("=" * 70)
    
    sample_examples = random.sample(unique_data, min(25, len(unique_data)))
    for i, example in enumerate(sample_examples, 1):
        print(f"{i:2d}. {example['original']} -> {example['styled']}")
    
    print(f"\n🎉 ФИНАЛЬНЫЙ МЕГА-ДАТАСЕТ ГОТОВ!")
    print(f"🚀 {len(unique_data)} КАЧЕСТВЕННЫХ ПРИМЕРОВ ДЛЯ СУПЕР-ОБУЧЕНИЯ!")
    print("💎 ГОТОВО К СОЗДАНИЮ ЛУЧШЕЙ ПИРАТСКОЙ МОДЕЛИ!")
    
    return unique_data

if __name__ == "__main__":
    final_dataset = create_final_mega_dataset()
    
    # Проверяем достигли ли цели в 1000+ примеров
    if len(final_dataset) >= 1000:
        print(f"\n🏆 ЦЕЛЬ ДОСТИГНУТА! {len(final_dataset)} примеров!")
    else:
        print(f"\n📊 Создано {len(final_dataset)} примеров")
        print(f"💡 Для достижения 1000+ нужно ещё {1000 - len(final_dataset)}")
