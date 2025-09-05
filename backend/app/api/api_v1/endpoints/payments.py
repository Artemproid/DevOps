from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.payment import (
    CreateCheckoutSession, 
    CheckoutSessionResponse, 
    SubscriptionStatus
)
from app.services.stripe_service import stripe_service

router = APIRouter()


@router.post("/create-checkout-session", response_model=CheckoutSessionResponse)
def create_checkout_session(
    checkout_data: CreateCheckoutSession,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Создает Stripe Checkout Session для оплаты премиум подписки
    """
    try:
        # Проверяем, есть ли уже премиум
        if current_user.is_premium:
            raise HTTPException(
                status_code=400, 
                detail="У вас уже есть премиум подписка! 🏴‍☠️"
            )
        
        # Создаем или получаем Stripe customer
        customer_id = current_user.stripe_customer_id
        print(f"🔍 DEBUG: current customer_id = {customer_id}")
        
        if not customer_id:
            print(f"🔍 DEBUG: Creating new customer for {current_user.email}")
            customer_id = stripe_service.create_customer(
                current_user.email, 
                current_user.username
            )
            print(f"🔍 DEBUG: Created customer_id = {customer_id}")
            
            if not customer_id:
                raise HTTPException(
                    status_code=500, 
                    detail="Ошибка создания customer в Stripe"
                )
            
            # Сохраняем customer_id в БД
            print(f"🔍 DEBUG: Saving customer_id to DB")
            crud.crud_user.update_stripe_customer(db, current_user.id, customer_id)
            print(f"🔍 DEBUG: Customer_id saved successfully")
        
        # Создаем Checkout Session
        print(f"🔍 DEBUG: Creating checkout session for customer {customer_id}")
        print(f"🔍 DEBUG: Success URL: {checkout_data.success_url}")
        print(f"🔍 DEBUG: Cancel URL: {checkout_data.cancel_url}")
        
        checkout_url = stripe_service.create_checkout_session(
            customer_id=customer_id,
            success_url=checkout_data.success_url,
            cancel_url=checkout_data.cancel_url
        )
        
        print(f"🔍 DEBUG: Received checkout_url = {checkout_url}")
        
        if not checkout_url:
            raise HTTPException(
                status_code=500, 
                detail="Ошибка создания платежной сессии"
            )
        
        return CheckoutSessionResponse(
            checkout_url=checkout_url,
            message="🏴‍☠️ Переходите к оплате, чтобы разблокировать пиратский режим!"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка создания платежа: {str(e)}"
        )


@router.get("/subscription-status", response_model=SubscriptionStatus)
def get_subscription_status(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получает статус подписки текущего пользователя
    """
    message = "🏴‍☠️ Премиум активен - пиратский режим доступен!" if current_user.is_premium else "⚓ Нужна подписка для пиратского режима"
    
    return SubscriptionStatus(
        is_premium=current_user.is_premium,
        stripe_customer_id=current_user.stripe_customer_id,
        stripe_subscription_id=current_user.stripe_subscription_id,
        message=message
    )


@router.post("/cancel-subscription")
def cancel_subscription(
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Отменяет премиум подписку
    """
    if not current_user.is_premium or not current_user.stripe_subscription_id:
        raise HTTPException(
            status_code=400, 
            detail="У вас нет активной подписки"
        )
    
    # Отменяем в Stripe
    success = stripe_service.cancel_subscription(current_user.stripe_subscription_id)
    if not success:
        raise HTTPException(
            status_code=500, 
            detail="Ошибка отмены подписки"
        )
    
    # Обновляем в БД
    crud.crud_user.update_subscription(db, current_user.id, None, False)
    
    return {"message": "⚓ Подписка отменена. Пиратский режим заблокирован!"}


@router.post("/test-activate-premium")
def test_activate_premium(
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    🧪 ТЕСТ: Активирует премиум статус для текущего пользователя
    Используй после успешной оплаты для проверки
    """
    try:
        # Активируем премиум
        crud.crud_user.update_subscription(
            db, 
            current_user.id, 
            subscription_id="manual_test_activation", 
            is_premium=True
        )
        
        return {
            "success": True,
            "message": "🏴‍☠️ Премиум активирован! Пиратский режим разблокирован!",
            "is_premium": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка активации премиума: {str(e)}"
        )


@router.post("/stripe-webhook")
async def stripe_webhook(request: Request, db: Session = Depends(deps.get_db)) -> Any:
    """
    Webhook endpoint для обработки событий от Stripe
    """
    try:
        payload = await request.body()
        signature = request.headers.get("stripe-signature")
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing signature")
        
        # Проверяем webhook
        event = stripe_service.verify_webhook(payload, signature)
        if not event:
            raise HTTPException(status_code=400, detail="Invalid webhook")
        
        # Обрабатываем событие
        success = stripe_service.handle_subscription_event(event, db)
        if not success:
            raise HTTPException(status_code=500, detail="Error processing event")
        
        return {"status": "success", "message": "Event processed"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Webhook error: {str(e)}"
        )
