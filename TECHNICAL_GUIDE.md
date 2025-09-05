# 🚀 ПОЛНОЕ ТЕХНИЧЕСКОЕ РУКОВОДСТВО ПРОЕКТА

## 📋 СТРУКТУРА ПРОЕКТА

```
pet/
├── docker-compose.yml          # Оркестрация всех сервисов
├── backend/                    # Python FastAPI сервер
│   ├── Dockerfile             # Контейнер для backend
│   ├── requirements.txt       # Python зависимости
│   ├── app/
│   │   ├── main.py           # 🎯 ТОЧКА ВХОДА BACKEND
│   │   ├── core/             # Основные компоненты
│   │   │   ├── websocket.py  # WebSocket manager
│   │   │   ├── redis_client.py # Redis клиент
│   │   │   ├── security.py   # JWT аутентификация
│   │   │   └── deps.py       # Dependency injection
│   │   ├── api/              # API endpoints
│   │   │   └── api_v1/
│   │   │       ├── api.py    # 🛣️ ГЛАВНЫЙ РОУТЕР
│   │   │       └── endpoints/
│   │   │           ├── auth.py      # Регистрация/логин
│   │   │           ├── users.py     # Управление пользователями  
│   │   │           ├── chats.py     # Чаты
│   │   │           ├── messages.py  # Сообщения
│   │   │           ├── websocket.py # WebSocket endpoint
│   │   │           └── system.py    # Мониторинг системы
│   │   ├── models/           # SQLAlchemy модели
│   │   │   ├── user.py       # Модель пользователя
│   │   │   ├── chat.py       # Модели чатов
│   │   │   └── message.py    # Модель сообщений
│   │   ├── schemas/          # Pydantic схемы
│   │   │   ├── user.py       # Схемы пользователей
│   │   │   ├── chat.py       # Схемы чатов
│   │   │   ├── message.py    # Схемы сообщений
│   │   │   └── websocket.py  # Схемы WebSocket
│   │   ├── crud/             # Database operations
│   │   │   ├── crud_user.py  # CRUD для пользователей
│   │   │   ├── crud_chat.py  # CRUD для чатов
│   │   │   └── crud_message.py # CRUD для сообщений
│   │   └── db/               # База данных
│   │       ├── base.py       # Импорты моделей
│   │       └── session.py    # Подключение к БД
├── frontend/                   # React приложение
│   ├── Dockerfile             # Контейнер для frontend
│   ├── package.json           # JavaScript зависимости
│   ├── src/
│   │   ├── index.js          # 🎯 ТОЧКА ВХОДА FRONTEND
│   │   ├── App.js            # 🛣️ ГЛАВНЫЙ РОУТЕР
│   │   ├── components/       # React компоненты
│   │   │   ├── Auth/         # Аутентификация
│   │   │   │   ├── Login.js
│   │   │   │   └── Register.js
│   │   │   ├── Chat/         # Чат компоненты
│   │   │   │   ├── ChatLayout.js   # Основной layout
│   │   │   │   ├── ChatBox.js      # Чат интерфейс
│   │   │   │   ├── ChatList.js     # Список чатов
│   │   │   │   ├── MessageList.js  # Список сообщений
│   │   │   │   └── OnlineUsers.js  # Онлайн пользователи
│   │   │   ├── Layout/       # Layout компоненты
│   │   │   │   └── Header.js # Шапка с поиском
│   │   │   └── UserSearch/   # Поиск пользователей
│   │   │       └── UserSearch.js
│   │   ├── services/         # API клиенты
│   │   │   ├── auth.service.js    # Аутентификация API
│   │   │   ├── user.service.js    # Пользователи API
│   │   │   ├── chat.service.js    # Чаты API
│   │   │   ├── message.service.js # Сообщения API
│   │   │   └── websocket.service.js # WebSocket клиент
│   │   ├── context/          # React Context
│   │   │   └── AuthContext.js # Состояние аутентификации
│   │   ├── hooks/            # Custom hooks
│   │   │   └── useAuth.js    # Hook для аутентификации
│   │   └── utils/            # Утилиты
│   │       └── axios.js      # HTTP клиент
└── Redis                      # In-memory база данных
    └── redis_data/           # Персистентные данные
```

---

## 🚀 ЗАПУСК СИСТЕМЫ: ШАГ ЗА ШАГОМ

### 1. 🐳 Docker Compose - Оркестратор всего

**Файл:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  # 🔧 Backend сервис
  backend:
    build: ./backend           # Собирается из ./backend/Dockerfile
    ports:
      - "8080:8000"           # Порт 8080 на хосте → 8000 в контейнере
    volumes:
      - ./backend:/app        # Live reload для разработки
    environment:              # Переменные окружения
      - DATABASE_URL=sqlite:///./social_network.db
      - REDIS_HOST=redis      # Имя Redis сервиса
      - REDIS_PORT=6379
      - REDIS_DB=0
    depends_on:
      - redis                 # Ждём запуска Redis
    restart: always

  # 🎨 Frontend сервис  
  frontend:
    build: ./frontend         # Собирается из ./frontend/Dockerfile
    ports:
      - "3000:3000"          # React dev server
    volumes:
      - ./frontend:/app       # Live reload для разработки
      - /app/node_modules     # Кэш node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true     # Hot reload на Windows
      - REACT_APP_API_URL=http://backend:8000
    depends_on:
      - backend
    restart: always

  # 📡 Redis сервис
  redis:
    image: redis:7-alpine     # Готовый образ Redis
    ports:
      - "6379:6379"          # Стандартный порт Redis
    volumes:
      - redis_data:/data      # Персистентное хранение
    restart: always
    command: redis-server --appendonly yes  # Включаем persistence

volumes:
  redis_data:                 # Named volume для Redis
```

**Команда запуска:**
```bash
docker-compose up -d
```

---

## 🔧 BACKEND: ДЕТАЛЬНЫЙ РАЗБОР

### 1. 🎯 Точка входа: `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router  # 👈 Импортируем все роуты

# Создаём FastAPI приложение
app = FastAPI(
    title="Social Network API",
    version="1.0.0",
    description="API для социальной сети с real-time чатом"
)

# CORS для связи frontend-backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем все API routes с префиксом /api
app.include_router(api_router, prefix="/api")

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Social Network API is running!"}
```

**Что происходит при запуске:**
1. FastAPI создаёт ASGI сервер
2. Загружаются все роуты из `api_router`
3. Настраивается CORS для frontend
4. Запускается на `0.0.0.0:8000` в контейнере

### 2. 🛣️ Главный роутер: `backend/app/api/api_v1/api.py`

```python
from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,        # /api/auth/*
    users,       # /api/users/*  
    chats,       # /api/chats/*
    messages,    # /api/messages/*
    websocket,   # /api/ws/*
    system       # /api/system/*
)

api_router = APIRouter()

# Регистрируем все endpoints с префиксами
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
```

### 3. 🔐 Аутентификация: `backend/app/api/api_v1/endpoints/auth.py`

**Ключевые endpoints:**

```python
@router.post("/register", response_model=schemas.User)
def register(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    # 1. Проверяем, не существует ли пользователь
    user = crud.crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Создаём пользователя с хэшированным паролем
    user = crud.crud_user.create_user(db, obj_in=user_in)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    # 1. Проверяем credentials
    user = crud.crud_user.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # 2. Создаём JWT token
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
```

### 4. 💬 WebSocket: `backend/app/api/api_v1/endpoints/websocket.py`

**Основной WebSocket endpoint:**

```python
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    # 1. Подключение к БД
    db = SessionLocal()
    
    try:
        # 2. Аутентификация по JWT токену ДО accept()
        current_user = await get_current_user_from_token(token, db)
        if not current_user:
            await websocket.close(code=4001, reason="Invalid token")
            return
            
        # 3. Принимаем WebSocket соединение
        await websocket.accept()
        user_id = current_user.id
        
        # 4. Регистрируем пользователя в ConnectionManager
        await manager.connect(websocket, user_id, current_user.username)
        
        # 5. Основной цикл обработки сообщений
        while True:
            try:
                # Получаем JSON от клиента
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Обрабатываем разные типы сообщений
                await handle_websocket_message(user_id, message_data, db)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket message error: {e}")
                
    finally:
        # 6. Очистка при отключении
        if 'user_id' in locals() and 'current_user' in locals():
            await manager.disconnect(user_id, current_user.username)
        db.close()
```

**Обработка сообщений:**

```python
async def handle_websocket_message(user_id: int, message_data: dict, db: Session):
    message_type = message_data.get("type")
    
    if message_type == "join_chat":
        # Присоединение к чату
        chat_id = message_data.get("chat_id")
        await manager.join_chat(user_id, chat_id)
        
    elif message_type == "send_message":
        # Отправка сообщения
        chat_id = message_data.get("chat_id")
        content = message_data.get("content")
        
        # Создаём сообщение в БД
        message_create = MessageCreate(content=content, chat_id=chat_id)
        message = crud.crud_message.create_message(db, obj_in=message_create, user_id=user_id)
        
        # Рассылаем через WebSocket
        await manager.broadcast_new_message(chat_id, message_dict)
    
    elif message_type == "typing_start":
        # Индикатор печатания
        chat_id = message_data.get("chat_id")
        await manager.set_typing_status(user_id, chat_id, True)
```

### 5. 🔧 ConnectionManager: `backend/app/core/websocket.py`

**Управление WebSocket соединениями:**

```python
class ConnectionManager:
    def __init__(self):
        # Активные соединения: {user_id: WebSocket}
        self.active_connections: Dict[int, WebSocket] = {}
        # Пользователи в чатах: {chat_id: Set[user_id]}
        self.chat_participants: Dict[int, Set[int]] = {}
        # Статус печатания: {chat_id: {user_id: True}}
        self.typing_users: Dict[int, Dict[int, bool]] = {}
        # Онлайн пользователи
        self.online_users: Set[int] = set()

    async def connect(self, websocket: WebSocket, user_id: int, username: str = None):
        # Закрываем старое соединение если есть
        if user_id in self.active_connections:
            old_websocket = self.active_connections[user_id]
            await old_websocket.close(code=1000, reason="New connection")
        
        # Сохраняем новое соединение
        self.active_connections[user_id] = websocket
        self.online_users.add(user_id)
        
        # Обновляем Redis
        set_user_online(user_id, username)
        
        # Уведомляем других пользователей
        await self.broadcast_user_status(user_id, "online", username)

    async def send_personal_message(self, user_id: int, message: dict):
        # Отправляем сообщение конкретному пользователю
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(json.dumps(message))

    async def broadcast_to_chat(self, chat_id: int, message: dict):
        # Рассылаем сообщение всем участникам чата
        if chat_id in self.chat_participants:
            for user_id in self.chat_participants[chat_id]:
                await self.send_personal_message(user_id, message)
```

### 6. 📡 Redis интеграция: `backend/app/core/redis_client.py`

**Redis клиент для кэширования и событий:**

```python
class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'redis'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )

    def set_user_online(self, user_id: int, username: str) -> bool:
        # Добавляем в set онлайн пользователей
        self.redis_client.sadd("online_users", user_id)
        
        # Сохраняем данные пользователя
        self.redis_client.setex(f"user:{user_id}:data", 3600, json.dumps({
            "id": user_id,
            "username": username,
            "status": "online"
        }))

    def publish_event(self, channel: str, event_type: str, data: dict):
        # Публикуем событие в Redis PubSub
        message = {"event_type": event_type, "data": data}
        self.redis_client.publish(channel, json.dumps(message))
```

### 7. 💾 База данных: SQLAlchemy модели

**User модель (`backend/app/models/user.py`):**

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    messages = relationship("Message", back_populates="user")
    chat_participations = relationship("ChatParticipant", back_populates="user")
```

**Chat модель (`backend/app/models/chat.py`):**

```python
class ChatType(str, Enum):
    PUBLIC = "PUBLIC"    # Общий чат
    PRIVATE = "PRIVATE"  # Приватный чат между 2 пользователями

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # NULL для приватных чатов
    chat_type = Column(Enum(ChatType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Связи
    messages = relationship("Message", back_populates="chat")
    participants = relationship("ChatParticipant", back_populates="chat")

class ChatParticipant(Base):
    __tablename__ = "chat_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User")
    chat = relationship("Chat", back_populates="participants")
```

---

## 🎨 FRONTEND: ДЕТАЛЬНЫЙ РАЗБОР

### 1. 🎯 Точка входа: `frontend/src/index.js`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';  // 👈 Глобальное состояние
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>  {/* Оборачиваем всё приложение в AuthContext */}
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

### 2. 🛣️ Главный роутер: `frontend/src/App.js`

```javascript
import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Layout/Header';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import ChatLayout from './components/Chat/ChatLayout';
import { useAuth } from './hooks/useAuth';

function App() {
  const { isAuthenticated } = useAuth();  // 👈 Проверяем аутентификацию

  return (
    <div className="App">
      <Header />
      <Routes>
        {/* Защищённые роуты */}
        <Route path="/chat" element={
          isAuthenticated ? <ChatLayout /> : <Navigate to="/login" />
        } />
        <Route path="/chat/:userId" element={
          isAuthenticated ? <ChatLayout /> : <Navigate to="/login" />
        } />
        
        {/* Публичные роуты */}
        <Route path="/login" element={
          !isAuthenticated ? <Login /> : <Navigate to="/chat" />
        } />
        <Route path="/register" element={
          !isAuthenticated ? <Register /> : <Navigate to="/chat" />
        } />
        
        {/* Редиректы */}
        <Route path="/" element={<Navigate to="/chat" />} />
        <Route path="*" element={<Navigate to="/chat" />} />
      </Routes>
    </div>
  );
}
```

### 3. 🔐 Аутентификация: `frontend/src/context/AuthContext.js`

```javascript
import React, { createContext, useState, useEffect } from 'react';
import authService from '../services/auth.service';
import websocketService from '../services/websocket.service';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Проверяем токен при загрузке приложения
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // Получаем данные пользователя
          const userData = await authService.getCurrentUser();
          setCurrentUser(userData);
          setIsAuthenticated(true);
          
          // Подключаемся к WebSocket
          websocketService.connect(token);
        } catch (error) {
          // Токен недействителен
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    const response = await authService.login(email, password);
    const { access_token } = response;
    
    // Сохраняем токен
    localStorage.setItem('token', access_token);
    
    // Получаем данные пользователя
    const userData = await authService.getCurrentUser();
    setCurrentUser(userData);
    setIsAuthenticated(true);
    
    // Подключаемся к WebSocket
    websocketService.connect(access_token);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setCurrentUser(null);
    setIsAuthenticated(false);
    websocketService.disconnect();  // 👈 Закрываем WebSocket
  };

  return (
    <AuthContext.Provider value={{
      currentUser,
      isAuthenticated,
      loading,
      login,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### 4. 📡 WebSocket клиент: `frontend/src/services/websocket.service.js`

```javascript
class WebSocketService {
  constructor() {
    this.ws = null;
    this.token = null;
    this.url = 'ws://localhost:8080/api/ws/ws';
    this.listeners = {};  // Event listeners
  }

  connect(token) {
    // Проверяем, не подключены ли уже
    if (this.ws && this.ws.readyState === WebSocket.OPEN && this.token === token) {
      return;
    }

    this.token = token;
    this.ws = new WebSocket(`${this.url}?token=${encodeURIComponent(token)}`);
    
    this.ws.onopen = (event) => {
      console.log('✅ WebSocket connected');
      this.emit('connected', event);
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('📨 Received:', data);
      
      // Эмитируем событие по типу сообщения
      this.emit(data.type, data);
    };

    this.ws.onclose = (event) => {
      console.log('❌ WebSocket disconnected:', event.code);
      this.emit('disconnected', event);
    };
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  // Event system
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data));
    }
  }

  // Chat methods
  joinChat(chatId) {
    this.send({ type: 'join_chat', chat_id: chatId });
  }

  sendMessage(chatId, content) {
    this.send({ type: 'send_message', chat_id: chatId, content });
  }

  startTyping(chatId) {
    this.send({ type: 'typing_start', chat_id: chatId });
  }
}

// Singleton
const websocketService = new WebSocketService();
export default websocketService;
```

### 5. 💬 Чат компонент: `frontend/src/components/Chat/ChatBox.js`

```javascript
function ChatBox() {
  const { userId } = useParams();  // ID собеседника из URL
  const { currentUser } = useAuth();
  
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [currentChat, setCurrentChat] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  // Загружаем чат при изменении userId
  useEffect(() => {
    const loadChat = async () => {
      if (userId) {
        // Приватный чат
        const chat = await chatService.getOrCreatePrivateChat(userId);
        setCurrentChat(chat);
        
        // Загружаем сообщения
        const chatMessages = await messageService.getPrivateMessages(userId);
        setMessages(chatMessages);
      } else {
        // Общий чат
        const chat = await chatService.getPublicChat();
        setCurrentChat(chat);
        
        const chatMessages = await messageService.getMessages();
        setMessages(chatMessages);
      }
    };

    loadChat();
  }, [userId]);

  // WebSocket события
  useEffect(() => {
    const handleNewMessage = (data) => {
      if (data.chat_id === currentChat?.id) {
        setMessages(prev => [...prev, data.message]);
      }
    };

    const handleConnected = () => setIsConnected(true);
    const handleDisconnected = () => setIsConnected(false);

    // Подписываемся на события
    websocketService.on('new_message', handleNewMessage);
    websocketService.on('connected', handleConnected);
    websocketService.on('disconnected', handleDisconnected);

    return () => {
      // Отписываемся при размонтировании
      websocketService.off('new_message', handleNewMessage);
      websocketService.off('connected', handleConnected);
      websocketService.off('disconnected', handleDisconnected);
    };
  }, [currentChat]);

  // Присоединяемся к чату через WebSocket
  useEffect(() => {
    if (currentChat && isConnected) {
      websocketService.joinChat(currentChat.id);
    }
  }, [currentChat, isConnected]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !currentChat) return;

    try {
      // Отправляем через API
      await messageService.createMessage({
        content: newMessage,
        chat_id: currentChat.id
      });
      
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <Card className="chat-card">
      <Card.Header>
        <h5>{userId ? `Чат с ${chatPartner?.username}` : 'Общий чат'}</h5>
        <Badge bg={isConnected ? 'success' : 'danger'}>
          {isConnected ? '🟢 Подключен' : '🔴 Отключен'}
        </Badge>
      </Card.Header>
      
      <Card.Body>
        <MessageList messages={messages} currentUser={currentUser} />
      </Card.Body>
      
      <Card.Footer>
        <Form onSubmit={handleSendMessage}>
          <Form.Control
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Введите сообщение..."
          />
          <Button type="submit">Отправить</Button>
        </Form>
      </Card.Footer>
    </Card>
  );
}
```

---

## 🔄 ЖИЗНЕННЫЙ ЦИКЛ СООБЩЕНИЯ

### 1. 📝 Пользователь пишет сообщение

```
Frontend: ChatBox.js
  ↓ handleSendMessage()
  ↓ messageService.createMessage()
  ↓ HTTP POST /api/messages/
```

### 2. 🔧 Backend обрабатывает запрос

```
Backend: messages.py
  ↓ create_message()
  ↓ crud_message.create_message() → SQLAlchemy → SQLite
  ↓ manager.broadcast_new_message() → WebSocket рассылка
```

### 3. 📡 WebSocket рассылка

```
Backend: websocket.py
  ↓ ConnectionManager.broadcast_to_chat()
  ↓ send_personal_message() для каждого участника
  ↓ websocket.send_text(JSON)
```

### 4. 📱 Frontend получает сообщение

```
Frontend: websocket.service.js
  ↓ onmessage event
  ↓ emit('new_message', data)
  ↓ ChatBox.js handleNewMessage()
  ↓ setMessages(prev => [...prev, newMessage])
  ↓ React re-render
```

---

## 🚀 ПОСЛЕДОВАТЕЛЬНОСТЬ ЗАПУСКА

### 1. `docker-compose up -d`
- Создаёт Docker сеть
- Запускает Redis контейнер
- Собирает и запускает Backend
- Собирает и запускает Frontend

### 2. Backend запуск (`backend/main.py`)
```
uvicorn app.main:app
  ↓ FastAPI app создаётся
  ↓ CORS middleware
  ↓ Подключение всех роутеров
  ↓ Подключение к SQLite
  ↓ Подключение к Redis
  ↓ Сервер слушает на :8000
```

### 3. Frontend запуск (`frontend/src/index.js`)
```
React App
  ↓ BrowserRouter
  ↓ AuthProvider (проверка токена)
  ↓ App.js роутинг
  ↓ Компоненты рендерятся
  ↓ Dev server на :3000
```

### 4. WebSocket соединение
```
User Login
  ↓ AuthContext.login()
  ↓ websocketService.connect(token)
  ↓ WebSocket('/api/ws/ws?token=xxx')
  ↓ Backend: websocket.py
  ↓ JWT аутентификация
  ↓ manager.connect()
  ↓ Redis: set_user_online()
  ↓ Broadcast user_status
```

---

## 🔍 ОТЛАДКА И МОНИТОРИНГ

### 1. Логи Backend
```bash
docker-compose logs backend -f
```

### 2. Логи Frontend  
```bash
docker-compose logs frontend -f
```

### 3. Redis мониторинг
```bash
docker exec -it pet-redis-1 redis-cli
redis-cli> KEYS *
redis-cli> SMEMBERS online_users
redis-cli> GET user:1:data
```

### 4. Health checks
- Backend health: `http://localhost:8080/api/system/health`
- System metrics: `http://localhost:8080/api/system/metrics`
- Redis info: `http://localhost:8080/api/system/redis/info`

---

## 📊 АРХИТЕКТУРНАЯ ДИАГРАММА

```
[Browser] ←HTTP→ [Frontend:3000] ←HTTP/WS→ [Backend:8080] ←TCP→ [Redis:6379]
    ↓                                           ↓
[React App]                              [FastAPI + SQLite]
    ↓                                           ↓
[WebSocket.js] ←WebSocket→ [ConnectionManager] ←Events→ [Redis PubSub]
```

### Поток данных:
1. **HTTP запросы**: Frontend → Backend (REST API)
2. **WebSocket**: Frontend ↔ Backend (real-time)
3. **База данных**: Backend ↔ SQLite (persistence)
4. **Кэш/События**: Backend ↔ Redis (performance/events)

---

## 🛠️ КАК САМОСТОЯТЕЛЬНО ВОССОЗДАТЬ

### 1. Создать структуру проекта
```bash
mkdir social-network
cd social-network
mkdir backend frontend
```

### 2. Backend setup
```bash
cd backend
pip install fastapi uvicorn sqlalchemy redis
# Создать все файлы по образцу выше
```

### 3. Frontend setup  
```bash
cd frontend
npx create-react-app .
npm install react-router-dom axios bootstrap react-bootstrap
# Создать все файлы по образцу выше
```

### 4. Docker setup
```bash
# Создать docker-compose.yml
# Создать Dockerfile для backend и frontend
docker-compose up -d
```

### 5. Тестирование
- Открыть http://localhost:3000
- Зарегистрировать пользователей
- Тестировать чат функционал

---

**Это полное техническое описание всей системы! 🚀**

Каждый файл, каждая функция, каждое соединение объяснено с примерами кода.
