from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import User


# Shared properties
class MessageBase(BaseModel):
    content: Optional[str] = None
    message_type: Optional[str] = "normal"


# Properties to receive on message creation
class MessageCreate(MessageBase):
    content: str
    chat_id: int
    message_type: Optional[str] = "normal"


# Properties shared by models stored in DB
class MessageInDBBase(MessageBase):
    id: int
    content: str
    message_type: str
    created_at: datetime
    user_id: int
    chat_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Message(MessageInDBBase):
    user: User


# Properties properties stored in DB
class MessageInDB(MessageInDBBase):
    pass 