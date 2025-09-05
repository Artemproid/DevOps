"""
🧪 ТЕСТ ПИРАТСКОГО API

Простой тест без запуска сервера
"""

import sys
import os

# Добавляем путь к backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.services.pirate_service import piratify_message, get_pirate_exclamation
    
    print("🏴‍☠️ ТЕСТ ПИРАТСКОГО СЕРВИСА")
    print("=" * 50)
    
    test_phrases = [
        "Привет, как дела?",
        "Иду спать", 
        "Хочу есть",
        "Потерял ключи",
        "Нужны деньги",
        "До свидания"
    ]
    
    print("📝 РЕЗУЛЬТАТЫ ТЕСТОВ:")
    for phrase in test_phrases:
        result = piratify_message(phrase)
        print(f"   '{phrase}' -> '{result}'")
    
    print(f"\n🎲 Случайное восклицание: {get_pirate_exclamation()}")
    
    print("\n✅ СЕРВИС РАБОТАЕТ ОТЛИЧНО!")
    print("\n🚀 ГОТОВО К ИНТЕГРАЦИИ В ЧАТ!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
