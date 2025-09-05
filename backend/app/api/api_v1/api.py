from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, messages, users, ascii_art, chats, websocket, system, pirate, payments
from app.api.api_v1.endpoints import ascii_art as ascii_art_generator

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
# Удаляем старый ascii_art роутер - заменен на ascii_art_generator
# api_router.include_router(ascii_art.router, prefix="/ascii-art", tags=["ascii-art"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(pirate.router, prefix="/pirate", tags=["pirate"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(ascii_art_generator.router, prefix="/ascii-generator", tags=["ascii-generator"]) 