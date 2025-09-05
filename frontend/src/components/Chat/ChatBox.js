import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Form, Button, Card, Alert, Spinner, Badge } from 'react-bootstrap';
import MessageList from './MessageList';
import OnlineUsers from './OnlineUsers';
import PirateMode from './PirateMode';
import PiratePreview from './PiratePreview';
import PremiumSubscription from '../Payment/PremiumSubscription';
import ASCIIArtGenerator from '../ASCIIArt/ASCIIArtGenerator';
import MessageTypeSelector from './MessageTypeSelector';
import { MessageType } from './MessageFactory';
import chatService from '../../services/chat.service';
import messageService from '../../services/message.service';
import userService from '../../services/user.service';
import websocketService from '../../services/websocket.service';
import { useAuth } from '../../hooks/useAuth';
import './Chat.css';

function ChatBox() {
  const { userId } = useParams(); // ID пользователя для приватного чата
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const [currentChat, setCurrentChat] = useState(null);
  const [chatPartner, setChatPartner] = useState(null); // Для приватных чатов
  const [typingUsers, setTypingUsers] = useState([]); // Кто печатает
  const [onlineUsers, setOnlineUsers] = useState([]); // Онлайн пользователи
  const [isConnected, setIsConnected] = useState(false);
  const [showOnlineUsers, setShowOnlineUsers] = useState(false);
  
  // Пиратский режим
  const [pirateMode, setPirateMode] = useState(false);
  const [pirateTransformFunction, setPirateTransformFunction] = useState(null);
  
  // Премиум статус
  const [isPremium, setIsPremium] = useState(false);
  
  // Тип сообщения
  const [selectedMessageType, setSelectedMessageType] = useState(MessageType.REGULAR);
  
  const typingTimeoutRef = useRef(null);
  const messagesEndRef = useRef(null);
  const currentChatRef = useRef(null);
  const currentUserRef = useRef(null);

  // Обновляем рефы при изменении
  useEffect(() => {
    currentChatRef.current = currentChat;
  }, [currentChat]);

  useEffect(() => {
    currentUserRef.current = currentUser;
  }, [currentUser]);

  // Определяем тип чата
  const isPrivateChat = !!userId;
  const isPublicChat = !userId;

  // Инициализация WebSocket соединения (только один раз при монтировании)
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      websocketService.connect(token);
    }

    // Подписываемся на события WebSocket
    const handleConnected = () => {
      setIsConnected(true);
      console.log('🟢 ChatBox: WebSocket connected');
    };

    const handleDisconnected = () => {
      setIsConnected(false);
      console.log('🔴 ChatBox: WebSocket disconnected');
    };

    const handleNewMessage = (data) => {
      console.log('📨 New message for chat:', data.chat_id, 'current chat:', currentChatRef.current?.id);
      if (data.chat_id === currentChatRef.current?.id) {
        setMessages(prev => {
          // Проверяем, нет ли уже этого сообщения
          const exists = prev.find(msg => msg.id === data.message.id);
          if (exists) return prev;
          return [...prev, data.message];
        });
        setTimeout(scrollToBottom, 100); // Даём время на рендер
      }
    };

    const handleTypingUpdate = (data) => {
      if (data.chat_id === currentChatRef.current?.id) {
        setTypingUsers(data.typing_users.filter(id => id !== currentUserRef.current?.id));
      }
    };

    const handleUserStatus = (data) => {
      if (data.status === 'online') {
        setOnlineUsers(prev => [...new Set([...prev, data.user_id])]);
      } else {
        setOnlineUsers(prev => prev.filter(id => id !== data.user_id));
      }
    };

    const handleOnlineUsers = (data) => {
      setOnlineUsers(data.users);
    };

    // Подписываемся на события
    websocketService.on('connected', handleConnected);
    websocketService.on('disconnected', handleDisconnected);
    websocketService.on('new_message', handleNewMessage);
    websocketService.on('typing_update', handleTypingUpdate);
    websocketService.on('user_status', handleUserStatus);
    websocketService.on('online_users', handleOnlineUsers);

    // Отписываемся при размонтировании
    return () => {
      websocketService.off('connected', handleConnected);
      websocketService.off('disconnected', handleDisconnected);
      websocketService.off('new_message', handleNewMessage);
      websocketService.off('typing_update', handleTypingUpdate);
      websocketService.off('user_status', handleUserStatus);
      websocketService.off('online_users', handleOnlineUsers);
    };
  }, []); // Убираем зависимости!

  // Загрузка чата и сообщений
  useEffect(() => {
    loadChat();
  }, [userId]);

  // Обработчик события отправки ASCII из генератора
  useEffect(() => {
    const handleSendASCII = async (event) => {
      const { asciiArt, messageType } = event.detail;
      
      if (currentChat && asciiArt) {
        try {
          setSending(true);
          
          // Отправляем ASCII напрямую через API с правильным типом
          await messageService.sendMessage(asciiArt, currentChat.id, messageType);
          
          console.log('✅ ASCII отправлен напрямую!');
        } catch (err) {
          console.error('❌ Ошибка отправки ASCII:', err);
          setError('Ошибка при отправке ASCII арт');
        } finally {
          setSending(false);
        }
      }
    };

    document.addEventListener('sendASCII', handleSendASCII);
    
    return () => {
      document.removeEventListener('sendASCII', handleSendASCII);
    };
  }, [currentChat]); // eslint-disable-line react-hooks/exhaustive-deps

  // Присоединение к чату через WebSocket
  useEffect(() => {
    if (currentChat) {
      console.log('🔗 Joining chat:', currentChat.id);
      
      // Ждём подключения WebSocket если нужно
      const tryJoinChat = () => {
        if (websocketService.isConnected()) {
          websocketService.joinChat(currentChat.id);
          websocketService.getOnlineUsers();
        } else {
          // Попробуем снова через 500мс
          setTimeout(tryJoinChat, 500);
        }
      };
      
      tryJoinChat();

      return () => {
        if (websocketService.isConnected()) {
          console.log('🚪 Leaving chat:', currentChat.id);
          websocketService.leaveChat(currentChat.id);
        }
      };
    }
  }, [currentChat]);

  // Автоскролл к последнему сообщению
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChat = async () => {
    try {
      setLoading(true);
      setError('');
      
      let chat;
      
      if (isPrivateChat) {
        // Приватный чат
        chat = await chatService.getOrCreatePrivateChat(userId);
        
        // Загружаем информацию о собеседнике
        const partner = await userService.getUser(userId);
        setChatPartner(partner);
        
        // Загружаем сообщения
        const msgs = await messageService.getPrivateMessages(userId);
        setMessages(msgs);
      } else {
        // Общий чат
        chat = await chatService.getPublicChat();
        setChatPartner(null);
        
        // Загружаем сообщения
        const msgs = await messageService.getMessages();
        setMessages(msgs);
      }
      
      setCurrentChat(chat);
    } catch (err) {
      console.error('Error loading chat:', err);
      setError('Ошибка при загрузке чата');
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!newMessage.trim() || !currentChat) return;
    
    try {
      setSending(true);
      setError('');
      
      // Останавливаем typing indicator
      if (websocketService.isConnected()) {
        websocketService.stopTyping(currentChat.id);
      }
      
      // Определяем какой текст отправлять
      let messageToSend = newMessage.trim();
      
      // Если включен пиратский режим, стилизируем сообщение
      if (pirateMode && pirateTransformFunction) {
        try {
          const pirateResult = await pirateTransformFunction(messageToSend);
          messageToSend = pirateResult.pirate_text || pirateResult.styled || messageToSend;
        } catch (err) {
          console.error('Ошибка пиратской стилизации:', err);
          // Отправляем оригинальное сообщение если стилизация не удалась
        }
      }
      
      // Отправляем сообщение через HTTP API с типом (WebSocket будет уведомлять о новом сообщении)
      await messageService.sendMessage(messageToSend, currentChat.id, selectedMessageType);
      setNewMessage('');
      
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Ошибка при отправке сообщения');
    } finally {
      setSending(false);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setNewMessage(value);

    // Авто-размер для textarea
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';

    // Typing indicators
    if (currentChat && websocketService.isConnected()) {
      if (value.trim()) {
        websocketService.startTyping(currentChat.id);
        
        // Останавливаем typing через 2 секунды бездействия
        if (typingTimeoutRef.current) {
          clearTimeout(typingTimeoutRef.current);
        }
        
        typingTimeoutRef.current = setTimeout(() => {
          websocketService.stopTyping(currentChat.id);
        }, 2000);
      } else {
        websocketService.stopTyping(currentChat.id);
        if (typingTimeoutRef.current) {
          clearTimeout(typingTimeoutRef.current);
        }
      }
    }
  };

  const getChatTitle = () => {
    if (isPrivateChat && chatPartner) {
      return `Чат с ${chatPartner.username}`;
    }
    return 'Общий чат';
  };

  const getChatSubtitle = () => {
    if (isPrivateChat && chatPartner) {
      const isPartnerOnline = onlineUsers.includes(parseInt(userId));
      return `${chatPartner.email} • ${isPartnerOnline ? 'Онлайн' : 'Офлайн'}`;
    }
    return `Чат для всех пользователей • ${onlineUsers.length} онлайн`;
  };

  const getTypingText = () => {
    if (typingUsers.length === 0) return '';
    if (typingUsers.length === 1) return 'печатает...';
    if (typingUsers.length === 2) return 'печатают...';
    return `${typingUsers.length} печатают...`;
  };

  const handlePirateToggle = (transformFunction) => {
    if (transformFunction) {
      setPirateMode(true);
      setPirateTransformFunction(() => transformFunction);
    } else {
      setPirateMode(false);
      setPirateTransformFunction(null);
    }
  };

  if (loading) {
    return (
      <Card className="chat-card">
        <Card.Body className="text-center">
          <Spinner animation="border" />
          <div className="mt-2">Загрузка чата...</div>
        </Card.Body>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="chat-card">
        <Card.Body>
          <Alert variant="danger">
            {error}
            <div className="mt-2">
              <Button variant="outline-danger" size="sm" onClick={loadChat}>
                Попробовать снова
              </Button>
            </div>
          </Alert>
        </Card.Body>
      </Card>
    );
  }

  return (
    <div className="chat-container" style={{ height: '100%' }}>
      {/* Заголовок чата */}
      <Card className="chat-header mb-2">
        <Card.Body className="py-2">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h5 className="mb-0">{getChatTitle()}</h5>
              <small className="text-muted">{getChatSubtitle()}</small>
            </div>
            <div className="d-flex align-items-center gap-2">
              {isPrivateChat ? (
                <Badge bg="primary">Приватный</Badge>
              ) : (
                <Badge bg="success">Общий</Badge>
              )}
              {isConnected ? (
                <Badge bg="success" className="small">🟢 Подключен</Badge>
              ) : (
                <Badge bg="danger" className="small">🔴 Отключен</Badge>
              )}
              <Button 
                variant="outline-info" 
                size="sm"
                onClick={() => setShowOnlineUsers(!showOnlineUsers)}
                title="Показать онлайн пользователей"
              >
                👥 ({onlineUsers.length})
              </Button>
              
              {/* Пиратский режим */}
              <PirateMode onTextTransform={handlePirateToggle} isPremium={isPremium} />
            </div>
          </div>
        </Card.Body>
      </Card>

      {/* Премиум подписка */}
      <div className="premium-section">
        <PremiumSubscription onSubscriptionChange={setIsPremium} />
      </div>

      {/* Список сообщений */}
      <div className="messages-section">
        <Card className="h-100">
          <Card.Body className="d-flex flex-column h-100" style={{ padding: '1rem' }}>
            <div className="flex-grow-1 overflow-auto">
              {messages.length === 0 ? (
                <div className="text-center text-muted py-4">
                  <p>Сообщений пока нет</p>
                  <small>Станьте первым, кто напишет сообщение!</small>
                </div>
              ) : (
                <>
                  <MessageList messages={messages} currentUser={currentUser} />
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>
            
            {/* Typing indicator */}
            {typingUsers.length > 0 && (
              <div className="typing-indicator p-2">
                <small className="text-muted">
                  <em>{getTypingText()}</em>
                </small>
              </div>
            )}
          </Card.Body>
        </Card>
      </div>

      {/* Предпросмотр пиратского текста */}
      <PiratePreview 
        originalText={newMessage}
        transformFunction={pirateTransformFunction}
        isVisible={pirateMode && newMessage.trim().length > 0}
      />

      {/* ASCII Арт Генератор */}
      <ASCIIArtGenerator isPremium={isPremium} />

      {/* Форма отправки сообщения */}
      <div className="input-section">
        <Card className="mt-2">
        <Card.Body>
          {error && (
            <Alert variant="danger" className="mb-3">
              {error}
            </Alert>
          )}
          
          <Form onSubmit={handleSendMessage}>
            {/* Селектор типов сообщений */}
            <div className="d-flex align-items-center mb-2">
              <MessageTypeSelector
                selectedType={selectedMessageType}
                onTypeChange={setSelectedMessageType}
                isPremium={isPremium}
              />
              <small className="text-muted ms-2">
                Выберите тип сообщения
              </small>
            </div>
            
            <div className="d-flex gap-2">
              <Form.Control
                as="textarea"
                rows={1}
                placeholder={pirateMode ? "Введите сообщение (будет стилизовано по-пиратски)..." : "Введите сообщение..."}
                value={newMessage}
                onChange={handleInputChange}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage(e);
                  }
                }}
                disabled={sending || !isConnected}
                className="flex-grow-1"
                style={{
                  resize: 'none',
                  overflow: 'hidden',
                  minHeight: '38px',
                  ...(pirateMode ? { borderColor: '#ffa500', backgroundColor: '#fef7e0' } : {})
                }}
              />
              <Button 
                type="submit" 
                disabled={!newMessage.trim() || sending}
                variant={pirateMode ? "warning" : "primary"}
              >
                {sending ? (
                  <>
                    <Spinner size="sm" className="me-1" />
                    {pirateMode ? 'Отправляем arr!' : 'Отправка...'}
                  </>
                ) : (
                  pirateMode ? '🏴‍☠️ Отправить' : 'Отправить'
                )}
              </Button>
            </div>
          </Form>
          </Card.Body>
        </Card>
      </div>

      {/* Список онлайн пользователей */}
      <OnlineUsers isVisible={showOnlineUsers} />
    </div>
  );
}

export default ChatBox;
