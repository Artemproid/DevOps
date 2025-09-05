#!/bin/bash

echo "🚀 Starting application..."

# Инициализируем базу данных
echo "🔄 Initializing database..."
python init_db.py

echo "✅ Database ready!"

# Создаем тестового пользователя
echo "👤 Creating test user..."
python create_test_user.py

# Запускаем приложение
echo "🌟 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
