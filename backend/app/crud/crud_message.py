from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate


def get_message(db: Session, message_id: int) -> Optional[Message]:
    return db.query(Message).filter(Message.id == message_id).first()


def get_chat_messages(db: Session, chat_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
    """Получить сообщения конкретного чата"""
    return db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()


def create_message(db: Session, message_in: MessageCreate, user_id: int) -> Message:
    db_message = Message(
        content=message_in.content,
        user_id=user_id,
        chat_id=message_in.chat_id,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


# Backward compatibility functions
def get_messages(db: Session, skip: int = 0, limit: int = 100) -> List[Message]:
    """Backward compatibility - возвращает сообщения общего чата"""
    from app.crud.crud_chat import get_public_chat
    public_chat = get_public_chat(db)
    return get_chat_messages(db, public_chat.id, skip, limit) 