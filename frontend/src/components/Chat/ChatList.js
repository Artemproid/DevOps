import React, { useState, useEffect } from 'react';
import { Card, ListGroup, Badge, Spinner, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import chatService from '../../services/chat.service';
import websocketService from '../../services/websocket.service';
import './Chat.css';

function ChatList() {
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [onlineUsers, setOnlineUsers] = useState([]);
  const navigate = useNavigate();

  // Загрузка списка чатов
  const loadChats = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await chatService.getUserChatsDetailed();
      setChats(response);
    } catch (err) {
      console.error('Error loading chats:', err);
      setError('Ошибка загрузки чатов');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadChats();

    // Подписываемся на обновления онлайн пользователей
    const handleOnlineUsers = (data) => {
      setOnlineUsers(data.users || []);
    };

    const handleUserStatus = (data) => {
      setOnlineUsers(prev => {
        if (data.status === 'online') {
          const exists = prev.find(user => user.id === data.user_id);
          if (!exists) {
            return [...prev, { id: data.user_id, username: data.username }];
          }
        } else if (data.status === 'offline') {
          return prev.filter(user => user.id !== data.user_id);
        }
        return prev;
      });
    };

    // Обновляем список чатов при новых сообщениях
    const handleNewMessage = (data) => {
      loadChats(); // Перезагружаем чтобы обновить последние сообщения
    };

    websocketService.on('online_users', handleOnlineUsers);
    websocketService.on('user_status', handleUserStatus);
    websocketService.on('new_message', handleNewMessage);

    return () => {
      websocketService.off('online_users', handleOnlineUsers);
      websocketService.off('user_status', handleUserStatus);
      websocketService.off('new_message', handleNewMessage);
    };
  }, []);

  const handleChatClick = (chat) => {
    if (chat.chat_type === 'PUBLIC') {
      navigate('/chat');
    } else if (chat.chat_type === 'PRIVATE' && chat.chat_partner) {
      navigate(`/chat/${chat.chat_partner.id}`);
    }
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);

    if (diffInHours < 1) {
      return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    } else if (diffInHours < 24) {
      return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    } else {
      return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' });
    }
  };

  const isUserOnline = (userId) => {
    return onlineUsers.find(user => user.id === userId);
  };

  const truncateText = (text, maxLength = 50) => {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  if (loading) {
    return (
      <Card className="chat-list-card">
        <Card.Body className="text-center p-4">
          <Spinner animation="border" size="sm" />
          <div className="mt-2">Загрузка чатов...</div>
        </Card.Body>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="chat-list-card">
        <Card.Body>
          <Alert variant="danger">{error}</Alert>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card className="chat-list-card">
      <Card.Header>
        <h5 className="mb-0">💬 Мои чаты ({chats.length})</h5>
      </Card.Header>
      <Card.Body className="p-0">
        {chats.length === 0 ? (
          <div className="text-center p-4 text-muted">
            <div className="mb-2">📭</div>
            <div>Нет активных чатов</div>
            <small>Найдите пользователей через поиск сверху</small>
          </div>
        ) : (
          <ListGroup variant="flush">
            {chats.map((chat) => (
              <ListGroup.Item
                key={chat.id}
                action
                onClick={() => handleChatClick(chat)}
                className="chat-list-item"
              >
                <div className="d-flex justify-content-between align-items-start">
                  <div className="flex-grow-1">
                    <div className="d-flex align-items-center mb-1">
                      <strong className="chat-name">
                        {chat.chat_type === 'PUBLIC' ? '🌐 ' : '👤 '}
                        {chat.name}
                      </strong>
                      {chat.chat_type === 'PRIVATE' && chat.chat_partner && isUserOnline(chat.chat_partner.id) && (
                        <span className="online-badge ms-2" title="Онлайн"></span>
                      )}
                    </div>
                    {chat.last_message ? (
                      <div className="last-message">
                        <small className="text-muted">
                          <strong>{chat.last_message.user.username}:</strong>{' '}
                          {truncateText(chat.last_message.content)}
                        </small>
                      </div>
                    ) : (
                      <small className="text-muted">Нет сообщений</small>
                    )}
                  </div>
                  <div className="chat-meta">
                    {chat.last_message && (
                      <small className="text-muted">
                        {formatTime(chat.last_message.created_at)}
                      </small>
                    )}
                    {chat.chat_type === 'PUBLIC' && (
                      <Badge bg="success" className="ms-2">Общий</Badge>
                    )}
                  </div>
                </div>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Card.Body>
    </Card>
  );
}

export default ChatList;
