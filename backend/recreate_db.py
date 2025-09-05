"""
Скрипт для полного пересоздания базы данных
"""

import os
import sys
import time
from sqlalchemy import text

# Добавляем путь к app
sys.path.append('/app')

from app.db.session import engine
from app.db.base import Base
from app import models

# Получаем DATABASE_URL из env вместо settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./social_network.db")

def wait_for_db(max_retries=30):
    """Ждем когда база данных будет готова"""
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ База данных готова!")
            return True
        except Exception as e:
            print(f"⏳ Ожидание БД... попытка {i+1}/{max_retries}")
            time.sleep(1)
    return False

def recreate_database():
    print("🏗️ Подключаемся к базе данных...")
    
    # Для SQLite - удаляем файлы
    if DATABASE_URL.startswith("sqlite"):
        print("🗑️ Удаляем старую базу данных SQLite...")
        db_files = ["social_network.db", "/app/social_network.db"]
        for db_file in db_files:
            if os.path.exists(db_file):
                os.remove(db_file)
                print(f"✅ Удален файл: {db_file}")
    
    # Для PostgreSQL - ждем готовности
    else:
        print("🐘 Используем PostgreSQL...")
        if not wait_for_db():
            print("❌ Не удалось подключиться к базе данных!")
            return False
    
    print("🏗️ Пересоздаем таблицы...")
    
    # Пересоздаем все таблицы
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    print("🎉 База данных успешно пересоздана!")
    print("📋 Созданные таблицы:")
    
    # Показываем созданные таблицы
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    recreate_database()
