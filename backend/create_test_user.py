"""
Создание тестового пользователя для демонстрации
"""

import sys
sys.path.append('/app')

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import crud
from app.schemas.user import UserCreate

def create_test_user():
    db = SessionLocal()
    
    try:
        # Проверяем есть ли уже тестовый пользователь
        existing_user = crud.crud_user.get_user_by_username(db, "testuser")
        if existing_user:
            print("✅ Тестовый пользователь уже существует")
            return
        
        # Создаем тестового пользователя
        test_user_data = UserCreate(
            username="testuser",
            email="test@example.com", 
            password="testpass123"
        )
        
        user = crud.crud_user.create_user(db, test_user_data)
        print(f"🎉 Создан тестовый пользователь: {user.username} (ID: {user.id})")
        print("📝 Логин: testuser")
        print("🔑 Пароль: testpass123")
        
    except Exception as e:
        print(f"❌ Ошибка создания тестового пользователя: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
