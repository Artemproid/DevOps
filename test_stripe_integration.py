"""
🧪 ТЕСТ STRIPE ИНТЕГРАЦИИ

Простой тест для проверки работы платежной системы
"""

import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:8080/api"

def test_stripe_endpoints():
    """Тестируем Stripe endpoints"""
    
    print("🧪 ТЕСТ STRIPE ИНТЕГРАЦИИ")
    print("=" * 50)
    
    # Сначала нужно залогиниться
    print("1. 🔐 Логин...")
    login_data = {
        "username": "test_user",  # Замени на существующего пользователя
        "password": "test_password"
    }
    
    try:
        # Логин
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("   ✅ Логин успешен!")
            
            # Проверяем статус подписки
            print("2. 📊 Проверяем статус подписки...")
            response = requests.get(f"{BASE_URL}/payments/subscription-status", headers=headers)
            if response.status_code == 200:
                status = response.json()
                print(f"   Premium статус: {status['is_premium']}")
                print(f"   Сообщение: {status['message']}")
            else:
                print(f"   ❌ Ошибка получения статуса: {response.status_code}")
            
            # Тестируем пиратский режим
            print("3. 🏴‍☠️ Тестируем пиратский режим...")
            pirate_data = {"text": "Привет, как дела?"}
            response = requests.post(f"{BASE_URL}/pirate/transform", 
                                   json=pirate_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Пиратский режим работает!")
                print(f"   Результат: {result['pirate_text']}")
            elif response.status_code == 403:
                print("   🚫 Пиратский режим заблокирован - нужна подписка!")
                print(f"   Сообщение: {response.json()['detail']}")
                
                # Создаем checkout session
                print("4. 💳 Создаем сессию для оплаты...")
                checkout_data = {
                    "success_url": "http://localhost:3000/success",
                    "cancel_url": "http://localhost:3000/cancel"
                }
                response = requests.post(f"{BASE_URL}/payments/create-checkout-session",
                                       json=checkout_data, headers=headers)
                
                if response.status_code == 200:
                    checkout = response.json()
                    print(f"   ✅ Checkout URL создан!")
                    print(f"   URL: {checkout['checkout_url']}")
                    print(f"   Сообщение: {checkout['message']}")
                else:
                    print(f"   ❌ Ошибка создания checkout: {response.json()}")
            else:
                print(f"   ❌ Неожиданная ошибка: {response.status_code}")
                
        else:
            print(f"   ❌ Ошибка логина: {response.status_code}")
            print("   Создайте тестового пользователя через /api/auth/register")
            
    except requests.exceptions.ConnectionError:
        print("❌ Не могу подключиться к серверу!")
        print("Убедитесь что сервер запущен: docker-compose up")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_stripe_endpoints()
