from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_stripe_customer(db: Session, stripe_customer_id: str) -> Optional[User]:
    """Получить пользователя по Stripe customer ID"""
    return db.query(User).filter(User.stripe_customer_id == stripe_customer_id).first()


def update_subscription(db: Session, user_id: int, subscription_id: Optional[str], is_premium: bool) -> Optional[User]:
    """Обновить информацию о подписке пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.stripe_subscription_id = subscription_id
        user.is_premium = is_premium
        db.commit()
        db.refresh(user)
    return user


def update_stripe_customer(db: Session, user_id: int, stripe_customer_id: str) -> Optional[User]:
    """Обновить Stripe customer ID пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.stripe_customer_id = stripe_customer_id
        db.commit()
        db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def search_users(db: Session, query: str, skip: int = 0, limit: int = 20) -> List[User]:
    """
    Поиск пользователей по username или email (частичное совпадение)
    """
    return db.query(User).filter(
        or_(
            User.username.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%")
        )
    ).filter(User.is_active == True).offset(skip).limit(limit).all()


def update_profile(db: Session, user_id: int, avatar_url: Optional[str] = None, bio: Optional[str] = None) -> Optional[User]:
    """Обновить профиль пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if avatar_url is not None:
            user.avatar_url = avatar_url
        if bio is not None:
            user.bio = bio
        db.commit()
        db.refresh(user)
    return user 