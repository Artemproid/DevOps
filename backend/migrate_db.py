"""
Скрипт для миграции базы данных
Добавляет новые поля для Stripe интеграции
"""

import sqlite3
import os

def migrate_database():
    db_path = "social_network.db"
    
    # Проверяем существует ли база
    if not os.path.exists(db_path):
        print("✅ База данных не найдена, будет создана автоматически при запуске")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Проверяем есть ли уже новые поля
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"📋 Существующие поля в таблице user: {columns}")
        
        # Добавляем недостающие поля
        fields_to_add = [
            ("is_premium", "BOOLEAN DEFAULT 0"),
            ("stripe_customer_id", "VARCHAR"),
            ("stripe_subscription_id", "VARCHAR")
        ]
        
        for field_name, field_type in fields_to_add:
            if field_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE user ADD COLUMN {field_name} {field_type}")
                    print(f"✅ Добавлено поле: {field_name}")
                except sqlite3.OperationalError as e:
                    print(f"⚠️ Поле {field_name} уже существует или ошибка: {e}")
            else:
                print(f"✅ Поле {field_name} уже существует")
        
        conn.commit()
        print("🎉 Миграция завершена успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка миграции: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Начинаем миграцию базы данных...")
    migrate_database()
