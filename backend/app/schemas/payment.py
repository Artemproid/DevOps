from typing import Optional
from pydantic import BaseModel


class CreateCheckoutSession(BaseModel):
    """Схема для создания Checkout Session"""
    success_url: str
    cancel_url: str


class CheckoutSessionResponse(BaseModel):
    """Ответ с URL для оплаты"""
    checkout_url: str
    message: str = "Redirect to payment page"


class SubscriptionStatus(BaseModel):
    """Статус подписки пользователя"""
    is_premium: bool
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    message: str


class WebhookEvent(BaseModel):
    """Webhook событие от Stripe"""
    type: str
    data: dict
