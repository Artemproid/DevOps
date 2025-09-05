from typing import Optional, Any, List
from pydantic import BaseModel


class WebSocketMessage(BaseModel):
    type: str
    chat_id: Optional[int] = None
    content: Optional[str] = None
    data: Optional[Any] = None


class TypingStatus(BaseModel):
    type: str = "typing_update"
    chat_id: int
    typing_users: List[int]


class UserStatus(BaseModel):
    type: str = "user_status"
    user_id: int
    status: str  # "online" | "offline"


class NewMessageNotification(BaseModel):
    type: str = "new_message"
    chat_id: int
    message: dict


class OnlineUsersResponse(BaseModel):
    type: str = "online_users"
    users: List[int]


class ChatJoinedResponse(BaseModel):
    type: str = "chat_joined"
    chat_id: int
