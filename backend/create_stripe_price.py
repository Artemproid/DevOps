"""
Создание Price для продукта в Stripe
"""

import stripe
import os

# Настройка Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_key")

def create_price():
    product_id = "prod_SvtWULzCIz4wkR"  # Твой product ID
    
    try:
        # Создаем price для продукта
        price = stripe.Price.create(
            product=product_id,
            unit_amount=999,  # $9.99 в центах
            currency="usd",
            recurring={"interval": "month"}
        )
        
        print(f"✅ Price создан!")
        print(f"🆔 Price ID: {price.id}")
        print(f"💰 Цена: ${price.unit_amount/100}")
        print(f"📅 Период: {price.recurring.interval}")
        
        # Показываем что вставить в .env
        print(f"\n📝 Добавь в .env файл:")
        print(f"STRIPE_PREMIUM_PRICE_ID={price.id}")
        
    except Exception as e:
        print(f"❌ Ошибка создания price: {e}")

if __name__ == "__main__":
    create_price()
