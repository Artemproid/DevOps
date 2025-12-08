from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc

from app.models.chat import Chat, ChatParticipant, ChatType
from app.models.user import User
from app.models.message import Message
from app.schemas.chat import ChatCreate


def get_chat(db: Session, chat_id: int) -> Optional[Chat]:
    return db.query(Chat).filter(Chat.id == chat_id).first()


def get_user_chats(db: Session, user_id: int) -> List[Chat]:
    """Получить все чаты пользователя"""
    return db.query(Chat).join(ChatParticipant).filter(
        ChatParticipant.user_id == user_id,
        Chat.is_active == True
    ).order_by(Chat.updated_at.desc()).all()


def get_or_create_private_chat(db: Session, user1_id: int, user2_id: int) -> Chat:
    """Получить или создать приватный чат между двумя пользователями"""
    
    # Ищем существующий приватный чат между этими пользователями
    existing_chat = db.query(Chat).join(ChatParticipant, Chat.id == ChatParticipant.chat_id).filter(
        Chat.chat_type == ChatType.PRIVATE,
        Chat.is_active == True
    ).group_by(Chat.id).having(
        func.count(ChatParticipant.user_id) == 2
    ).filter(
        Chat.id.in_(
            db.query(ChatParticipant.chat_id).filter(ChatParticipant.user_id == user1_id)
        ),
        Chat.id.in_(
            db.query(ChatParticipant.chat_id).filter(ChatParticipant.user_id == user2_id)
        )
    ).first()
    
    if existing_chat:
        return existing_chat
    
    # Создаём новый приватный чат
    new_chat = Chat(
        chat_type=ChatType.PRIVATE,
        name=None
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    
    # Добавляем участников
    participant1 = ChatParticipant(chat_id=new_chat.id, user_id=user1_id)
    participant2 = ChatParticipant(chat_id=new_chat.id, user_id=user2_id)
    
    db.add(participant1)
    db.add(participant2)
    db.commit()
    
    return new_chat


def get_public_chat(db: Session) -> Chat:
    """Получить или создать общий чат"""
    public_chat = db.query(Chat).filter(
        Chat.chat_type == ChatType.PUBLIC,
        Chat.is_active == True
    ).first()
    
    if not public_chat:
        public_chat = Chat(
            chat_type=ChatType.PUBLIC,
            name="Общий чат",
            description="Общий чат для всех пользователей"
        )
        db.add(public_chat)
        db.commit()
        db.refresh(public_chat)
    
    return public_chat


def add_user_to_public_chat(db: Session, user_id: int):
    """Добавить пользователя в общий чат"""
    public_chat = get_public_chat(db)
    
    # Проверяем, не является ли пользователь уже участником
    existing_participant = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == public_chat.id,
        ChatParticipant.user_id == user_id
    ).first()
    
    if not existing_participant:
        participant = ChatParticipant(
            chat_id=public_chat.id,
            user_id=user_id
        )
        db.add(participant)
        db.commit()


def is_user_in_chat(db: Session, user_id: int, chat_id: int) -> bool:
    """Проверить, является ли пользователь участником чата"""
    participant = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == chat_id,
        ChatParticipant.user_id == user_id
    ).first()
    return participant is not None


def get_user_chats_with_details(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Получить чаты пользователя с дополнительной информацией"""
    
    # Получаем чаты пользователя с last message
    chats_query = db.query(Chat).join(ChatParticipant).filter(
        ChatParticipant.user_id == user_id,
        Chat.is_active == True
    )
    
    chats = chats_query.all()
    result = []
    
    for chat in chats:
        # Получаем последнее сообщение
        last_message = db.query(Message).filter(
            Message.chat_id == chat.id
        ).order_by(desc(Message.created_at)).first()
        
        # Получаем участников (для приватных чатов)
        participants = db.query(ChatParticipant).options(
            joinedload(ChatParticipant.user)
        ).filter(ChatParticipant.chat_id == chat.id).all()
        
        # Для приватных чатов находим собеседника
        chat_partner = None
        if chat.chat_type == ChatType.PRIVATE:
            for participant in participants:
                if participant.user_id != user_id:
                    chat_partner = participant.user
                    break
        
        # Формируем название чата
        chat_name = chat.name
        if chat.chat_type == ChatType.PRIVATE and chat_partner:
            chat_name = chat_partner.username
        elif chat.chat_type == ChatType.PUBLIC:
            chat_name = "Общий чат"
        
        result.append({
            "id": chat.id,
            "name": chat_name,
            "chat_type": chat.chat_type,
            "created_at": chat.created_at,
            "last_message": {
                "id": last_message.id,
                "content": last_message.content,
                "created_at": last_message.created_at,
                "user": {
                    "id": last_message.user.id,
                    "username": last_message.user.username
                }
            } if last_message else None,
            "participants_count": len(participants),
            "chat_partner": {
                "id": chat_partner.id,
                "username": chat_partner.username,
                "email": chat_partner.email
            } if chat_partner else None
        })
    
    # Сортируем по времени последнего сообщения (новые сверху)
    result.sort(key=lambda x: x["last_message"]["created_at"] if x["last_message"] else x["created_at"], reverse=True)
    
    return result
