"""
🎯 ШАГ 3: ОБУЧАЕМ МОДЕЛЬ НА НАШИХ ДАННЫХ

Что происходит:
1. Загружаем базовую модель ruGPT-3
2. Загружаем наши тренировочные данные
3. Fine-tuning модели на пиратском стиле
4. Сохраняем обученную модель
"""

import json
import torch
from transformers import (
    GPT2LMHeadModel, 
    GPT2Tokenizer, 
    Trainer, 
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import os
from tqdm import tqdm

class PirateDataset:
    """Класс для подготовки данных для обучения"""
    
    def __init__(self, tokenizer, max_length=128):
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def load_data(self, data_path):
        """Загружает и подготавливает данные"""
        
        print(f"📚 Загружаем данные из: {data_path}")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Найдено {len(data)} примеров")
        
        # Подготавливаем тексты для обучения
        texts = []
        for item in data:
            # Форматируем как: "Стиль пират: текст -> результат<|endoftext|>"
            text = item['text'] + self.tokenizer.eos_token
            texts.append(text)
        
        return texts
    
    def tokenize_data(self, texts):
        """Токенизирует данные"""
        
        print("🔤 Токенизируем данные...")
        
        tokenized_data = []
        
        for text in tqdm(texts, desc="Токенизация"):
            # Токенизируем
            encoded = self.tokenizer(
                text,
                truncation=True,
                padding='max_length',
                max_length=self.max_length,
                return_tensors="pt"
            )
            
            tokenized_data.append({
                'input_ids': encoded['input_ids'].squeeze(),
                'attention_mask': encoded['attention_mask'].squeeze(),
                'labels': encoded['input_ids'].squeeze()  # Для language modeling
            })
        
        return Dataset.from_list(tokenized_data)

def setup_model_and_tokenizer(model_path="../../rus_gpt2"):
    """Загружает модель и токенизатор"""
    
    print("🤖 Загружаем твою русскую модель...")
    
    try:
        # Загружаем твою модель
        model = GPT2LMHeadModel.from_pretrained(model_path)
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        
        print("✅ Твоя модель успешно загружена!")
        print(f"📊 Параметров: {sum(p.numel() for p in model.parameters()):,}")
        print(f"📖 Размер словаря: {tokenizer.vocab_size:,} токенов")
        
    except Exception as e:
        print(f"❌ Ошибка загрузки твоей модели: {e}")
        print("🔄 Пробуем загрузить запасную модель...")
        
        # Запасной вариант
        model_name = "sberbank-ai/rugpt3small_based_on_gpt2"
        model = GPT2LMHeadModel.from_pretrained(model_name)
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        print("✅ Запасная модель загружена")
    
    # Настраиваем токенизатор
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer

def train_pirate_model():
    """Основная функция обучения"""
    
    print("🏴‍☠️ НАЧИНАЕМ ОБУЧЕНИЕ ПИРАТСКОЙ МОДЕЛИ!")
    print("=" * 60)
    
    # 1. Загружаем модель
    model, tokenizer = setup_model_and_tokenizer()
    
    # 2. Подготавливаем данные
    dataset_helper = PirateDataset(tokenizer)
    texts = dataset_helper.load_data("./training_data/enhanced_pirate_data.json")
    train_dataset = dataset_helper.tokenize_data(texts)
    
    print(f"📊 Размер датасета: {len(train_dataset)} примеров")
    
    # 3. Настройки обучения
    training_args = TrainingArguments(
        output_dir="./pirate_model_checkpoints",
        overwrite_output_dir=True,
        
        # Основные параметры
        num_train_epochs=3,  # 3 эпохи - не много, но достаточно для fine-tuning
        per_device_train_batch_size=2,  # Маленький batch_size для GPU
        gradient_accumulation_steps=4,  # Накопление градиентов
        
        # Оптимизация
        learning_rate=5e-5,  # Небольшой learning rate для fine-tuning
        warmup_steps=100,
        
        # Сохранение
        save_steps=100,
        save_total_limit=3,
        
        # Логирование
        logging_steps=50,
        logging_dir="./logs",
        
        # Оценка
        evaluation_strategy="no",  # Пока без валидации
        
        # Другое
        prediction_loss_only=True,
        remove_unused_columns=False,
    )
    
    # 4. Data collator для language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # Не masked language modeling, а autoregressive
    )
    
    # 5. Создаём тренер
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    
    # 6. Проверяем устройство
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Устройство для обучения: {device}")
    
    if device == "cuda":
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"🎮 GPU: {gpu_name}")
        print(f"🎮 Память GPU: {gpu_memory:.1f} GB")
    else:
        print("⚠️  Обучение на CPU будет медленным!")
    
    # 7. НАЧИНАЕМ ОБУЧЕНИЕ!
    print(f"\n🚀 НАЧИНАЕМ ОБУЧЕНИЕ!")
    print("🍿 Иди попей чай, это займёт время...")
    
    try:
        trainer.train()
        print("✅ Обучение завершено успешно!")
        
        # 8. Сохраняем финальную модель
        final_model_path = "./pirate_model_final"
        trainer.save_model(final_model_path)
        tokenizer.save_pretrained(final_model_path)
        
        print(f"💾 Модель сохранена в: {final_model_path}")
        
        # 9. Тестируем модель
        test_model(model, tokenizer)
        
    except Exception as e:
        print(f"❌ Ошибка при обучении: {e}")
        print("\n💡 ВОЗМОЖНЫЕ РЕШЕНИЯ:")
        print("   - Уменьшить batch_size")
        print("   - Увеличить gradient_accumulation_steps")  
        print("   - Использовать CPU вместо GPU")
        print("   - Освободить память GPU")

def test_model(model, tokenizer):
    """Тестирует обученную модель"""
    
    print("\n🧪 ТЕСТИРУЕМ ОБУЧЕННУЮ МОДЕЛЬ:")
    print("=" * 50)
    
    test_phrases = [
        "Стиль пират: Привет, как дела? ->",
        "Стиль пират: Иду спать ->", 
        "Стиль пират: Хочу есть ->",
        "Стиль пират: Потерял ключи ->",
        "Стиль пират: Дорогие вещи ->"
    ]
    
    model.eval()
    
    for phrase in test_phrases:
        print(f"\n🔤 Входной текст: '{phrase}'")
        
        # Токенизируем
        inputs = tokenizer.encode(phrase, return_tensors="pt")
        
        # Генерируем
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 30,
                temperature=0.8,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                num_return_sequences=1
            )
        
        # Декодируем
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print(f"🎯 Результат: '{generated_text}'")

def get_training_info():
    """Показывает информацию о процессе обучения"""
    
    print("\n📋 ИНФОРМАЦИЯ О ПРОЦЕССЕ ОБУЧЕНИЯ:")
    print("=" * 60)
    
    print("🎯 ЧТО ПРОИСХОДИТ:")
    print("   1. Модель изучает паттерны: 'обычный текст -> пиратский'")
    print("   2. Каждый пример показывается модели много раз")
    print("   3. Модель корректирует свои 'нейроны' для лучшего результата")
    print("   4. После обучения модель сможет стилизовать новые тексты")
    
    print("\n⏱️  ВРЕМЯ ОБУЧЕНИЯ:")
    print("   📱 На CPU: 30-60 минут")
    print("   🎮 На GPU: 5-15 минут")
    
    print("\n📊 ПАРАМЕТРЫ:")
    print("   📚 Эпох: 3 (количество полных проходов по данным)")
    print("   📦 Batch size: 2 (примеров за раз)")
    print("   🧠 Learning rate: 5e-5 (скорость обучения)")
    
    print("\n🔍 КАК ПОНЯТЬ ЧТО ВСЁ РАБОТАЕТ:")
    print("   ✅ Loss должен уменьшаться")
    print("   ✅ Модель не должна выдавать одинаковый текст")
    print("   ✅ Результат должен быть читаемым")

if __name__ == "__main__":
    print("🏴‍☠️ ОПЕРАЦИЯ 'ПРОМЫВКА МОЗГОВ'")
    print("=" * 50)
    
    # Показываем информацию
    get_training_info()
    
    # Спрашиваем подтверждение
    print(f"\n🤔 Готов начать обучение? (y/n): ", end="")
    choice = input().lower().strip()
    
    if choice in ['y', 'yes', 'да', 'д']:
        train_pirate_model()
    else:
        print("👋 Хорошо, запустишь когда будешь готов!")
        print("💡 Команда: python step3_train_model.py")
