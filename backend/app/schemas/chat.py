from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import User


class ChatBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    chat_type: str = "private"


class ChatCreate(ChatBase):
    participant_ids: List[int]  # ID участников чата


class ChatInDBBase(ChatBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class Chat(ChatInDBBase):
    participants: Optional[List[User]] = []


class ChatInDB(ChatInDBBase):
    pass


# Participant schemas
class ChatParticipantBase(BaseModel):
    is_admin: bool = False


class ChatParticipantCreate(ChatParticipantBase):
    chat_id: int
    user_id: int


class ChatParticipant(ChatParticipantBase):
    id: int
    chat_id: int
    user_id: int
    joined_at: datetime
    user: Optional[User] = None

    class Config:
        orm_mode = True
