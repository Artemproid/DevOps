"""
🔤 СОЗДАНИЕ ТОКЕНИЗАТОРА ДЛЯ ТВОЕЙ МОДЕЛИ

У твоей модели нет токенизатора, создадим совместимый
"""

from transformers import GPT2Tokenizer
import os

def create_tokenizer_for_model():
    """Создаёт токенизатор для твоей модели"""
    
    print("🔤 Создаём токенизатор для твоей модели...")
    
    model_path = "../../rus_gpt2"
    
    # Используем стандартный русский токенизатор GPT-2
    print("📥 Скачиваем совместимый токенизатор...")
    tokenizer = GPT2Tokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
    
    # Сохраняем в папку твоей модели
    print(f"💾 Сохраняем токенизатор в: {model_path}")
    tokenizer.save_pretrained(model_path)
    
    print("✅ Токенизатор создан и сохранён!")
    
    # Тестируем
    test_text = "Привет, как дела?"
    tokens = tokenizer.encode(test_text)
    decoded = tokenizer.decode(tokens)
    
    print(f"\n🧪 ТЕСТ ТОКЕНИЗАТОРА:")
    print(f"   Текст: '{test_text}'")
    print(f"   Токены: {tokens}")
    print(f"   Обратно: '{decoded}'")
    
    return tokenizer

if __name__ == "__main__":
    create_tokenizer_for_model()


