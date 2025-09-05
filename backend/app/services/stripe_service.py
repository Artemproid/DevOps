import os
import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

# Импорт Stripe после установки переменных окружения
import stripe as stripe_sdk

from app import crud
from app.models.user import User

logger = logging.getLogger(__name__)

# Настройка Stripe
stripe_sdk.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_test_key_here")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_your_webhook_secret")

class StripeService:
    """Сервис для работы с платежами Stripe"""
    
    @staticmethod
    def create_customer(email: str, username: str) -> Optional[str]:
        """Создает customer в Stripe"""
        try:
            customer = stripe_sdk.Customer.create(
                email=email,
                name=username,
                metadata={"username": username}
            )
            logger.info(f"🔍 Raw customer object: {customer}")
            logger.info(f"🔍 Customer type: {type(customer)}")
            logger.info(f"🔍 Customer dir: {dir(customer)}")
            
            if hasattr(customer, 'id'):
                customer_id = customer.id
                logger.info(f"🎯 Stripe customer created: {customer_id} for {email}")
                return customer_id
            else:
                logger.error(f"❌ Customer object has no 'id' attribute")
                return None
        except Exception as e:
            logger.error(f"❌ Error creating Stripe customer: {e}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return None
    
    @staticmethod
    def create_subscription(customer_id: str, price_id: str = None) -> Optional[Dict[str, Any]]:
        """Создает подписку для customer"""
        try:
            # Используем тестовый price ID или дефолтный
            if not price_id:
                price_id = os.getenv("STRIPE_PREMIUM_PRICE_ID", "price_test_premium")
            
            subscription = stripe_sdk.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"]
            )
            
            return {
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret,
                "status": subscription.status
            }
        except Exception as e:
            logger.error(f"❌ Error creating subscription: {e}")
            return None
    
    @staticmethod
    def create_checkout_session(customer_id: str, success_url: str, cancel_url: str) -> Optional[str]:
        """Создает Checkout Session для оплаты"""
        try:
            price_id = os.getenv("STRIPE_PREMIUM_PRICE_ID", "price_test_premium")
            logger.info(f"🔧 Creating checkout with price_id: {price_id}")
            
            session = stripe_sdk.checkout.Session.create(
                customer=customer_id,
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                mode="subscription",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={"feature": "pirate_mode"}
            )
            
            logger.info(f"✅ Checkout session created: {session.id}")
            logger.info(f"🔗 Session URL: {session.url}")
            
            return session.url
        except Exception as e:
            logger.error(f"❌ Error creating checkout session: {e}")
            logger.error(f"🔧 price_id used: {os.getenv('STRIPE_PREMIUM_PRICE_ID')}")
            return None
    
    @staticmethod
    def cancel_subscription(subscription_id: str) -> bool:
        """Отменяет подписку"""
        try:
            stripe_sdk.Subscription.delete(subscription_id)
            logger.info(f"📅 Subscription cancelled: {subscription_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error cancelling subscription: {e}")
            return False
    
    @staticmethod
    def verify_webhook(payload: bytes, signature: str) -> Optional[Dict[str, Any]]:
        """Проверяет webhook от Stripe"""
        try:
            event = stripe_sdk.Webhook.construct_event(
                payload, signature, STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            logger.error(f"❌ Invalid payload in webhook: {e}")
            return None
        except stripe_sdk.error.SignatureVerificationError as e:
            logger.error(f"❌ Invalid signature in webhook: {e}")
            return None
    
    @staticmethod
    def handle_subscription_event(event: Dict[str, Any], db: Session) -> bool:
        """Обрабатывает события подписки"""
        try:
            event_type = event["type"]
            subscription = event["data"]["object"]
            customer_id = subscription.get("customer")
            
            # Находим пользователя по customer_id
            user = crud.crud_user.get_user_by_stripe_customer(db, customer_id)
            if not user:
                logger.warning(f"⚠️ User not found for customer_id: {customer_id}")
                return False
            
            if event_type == "customer.subscription.created":
                # Подписка создана
                crud.crud_user.update_subscription(
                    db, user.id, subscription["id"], is_premium=True
                )
                logger.info(f"✅ Premium activated for user {user.username}")
                
            elif event_type == "customer.subscription.deleted":
                # Подписка отменена
                crud.crud_user.update_subscription(
                    db, user.id, None, is_premium=False
                )
                logger.info(f"❌ Premium deactivated for user {user.username}")
                
            elif event_type == "invoice.payment_failed":
                # Платеж не прошел
                logger.warning(f"💸 Payment failed for user {user.username}")
                # Можно добавить логику уведомлений
                
            return True
        except Exception as e:
            logger.error(f"❌ Error handling subscription event: {e}")
            return False

# Создаем экземпляр сервиса
stripe_service = StripeService()
