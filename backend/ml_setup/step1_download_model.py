"""
🎯 ШАГ 1: ПИЗДИМ БАЗОВУЮ МОДЕЛЬ

Что происходит:
1. Скачиваем ruGPT-3 Small с Hugging Face
2. Сохраняем локально чтобы не скачивать каждый раз
3. Проверяем что всё работает
"""

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import os

def download_base_model():
    """Скачивает и сохраняет базовую модель"""
    
    print("🚀 Начинаем пиздить модель...")
    
    # Путь куда сохраним модель
    model_path = "./models/rugpt3_base"
    os.makedirs(model_path, exist_ok=True)
    
    try:
        print("📦 Скачиваем ruGPT-3 Small...")
        
        # Скачиваем модель и токенизатор
        model_name = "sberbank-ai/rugpt3small_based_on_gpt2"
        
        print(f"   Загружаем модель: {model_name}")
        model = GPT2LMHeadModel.from_pretrained(model_name)
        
        print(f"   Загружаем токенизатор...")
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        
        # Сохраняем локально
        print(f"💾 Сохраняем в: {model_path}")
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)
        
        print("✅ Модель успешно спизжена и сохранена!")
        
        # Проверяем что модель работает
        test_model(model, tokenizer)
        
    except Exception as e:
        print(f"❌ Ошибка при скачивании: {e}")
        print("💡 Возможные причины:")
        print("   - Нет интернета")
        print("   - Мало места на диске")
        print("   - Проблемы с Hugging Face")

def test_model(model, tokenizer):
    """Тестируем что модель работает"""
    
    print("\n🧪 Тестируем модель...")
    
    # Пробуем сгенерировать текст
    test_text = "Привет, как дела?"
    
    print(f"🔤 Входной текст: '{test_text}'")
    
    # Токенизируем текст
    inputs = tokenizer.encode(test_text, return_tensors="pt")
    print(f"🔢 Токены: {inputs.tolist()}")
    
    # Генерируем продолжение
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=inputs.shape[1] + 20,  # +20 новых токенов
            temperature=0.8,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Декодируем результат
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(f"🎯 Результат: '{generated_text}'")
    print("✅ Модель работает!")
    
    return generated_text

def get_model_info():
    """Показывает информацию о модели"""
    
    print("\n📊 ИНФОРМАЦИЯ О МОДЕЛИ:")
    print("=" * 50)
    
    model_path = "./models/rugpt3_base"
    
    if os.path.exists(model_path):
        print("✅ Модель найдена локально")
        
        # Загружаем для анализа
        model = GPT2LMHeadModel.from_pretrained(model_path)
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        
        # Считаем параметры
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"🧠 Всего параметров: {total_params:,}")
        print(f"🎯 Обучаемых параметров: {trainable_params:,}")
        print(f"📖 Размер словаря: {tokenizer.vocab_size:,} токенов")
        
        # Размер модели на диске
        model_size_mb = sum(
            os.path.getsize(os.path.join(model_path, f))
            for f in os.listdir(model_path)
            if os.path.isfile(os.path.join(model_path, f))
        ) / (1024 * 1024)
        
        print(f"💾 Размер на диске: {model_size_mb:.1f} MB")
        
        # Проверяем устройство
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🖥️  Устройство: {device}")
        
        if device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"🎮 GPU: {gpu_name}")
            print(f"🎮 Память GPU: {gpu_memory:.1f} GB")
        
    else:
        print("❌ Модель не найдена, запустите download_base_model()")

if __name__ == "__main__":
    print("🎭 ОПЕРАЦИЯ 'КРАЖА МОЗГОВ'")
    print("=" * 40)
    
    # Скачиваем модель
    download_base_model()
    
    # Показываем информацию
    get_model_info()
    
    print("\n🎉 ШАГ 1 ЗАВЕРШЁН!")
    print("📋 Следующий шаг: создание тренировочных данных")
