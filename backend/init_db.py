"""
Простая инициализация базы данных
"""

import os
import sys

# Добавляем путь к app
sys.path.append('/app')

def init_database():
    try:
        print("🚀 Инициализация базы данных...")
        
        # Импортируем здесь для избежания ошибок импорта
        from app.db.session import engine
        from app.db.base import Base
        
        # Импортируем все модели
        from app.models.user import User
        from app.models.chat import Chat
        from app.models.message import Message
        
        print("📋 Создаем таблицы...")
        
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        
        print("✅ База данных инициализирована!")
        print("📋 Созданные таблицы:")
        
        # Показываем созданные таблицы
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
