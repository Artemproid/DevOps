import React, { useState, useEffect } from 'react';
import websocketService from '../../services/websocket.service';
import './Chat.css';

const OnlineUsers = ({ isVisible }) => {
  const [onlineUsers, setOnlineUsers] = useState([]);

  useEffect(() => {
    // Запрашиваем список онлайн пользователей
    const fetchOnlineUsers = () => {
      if (websocketService.isConnected()) {
        websocketService.getOnlineUsers();
      }
    };

    // Обработчик списка онлайн пользователей
    const handleOnlineUsers = (data) => {
      console.log('📊 Online users received:', data);
      setOnlineUsers(data.users || []);
    };

    // Обработчик изменения статуса пользователя
    const handleUserStatus = (data) => {
      console.log('🟢 User status update:', data);
      setOnlineUsers(prev => {
        if (data.status === 'online') {
          // Добавляем пользователя если его нет в списке
          if (!prev.find(user => user.id === data.user_id)) {
            return [...prev, { id: data.user_id, username: data.username }];
          }
        } else if (data.status === 'offline') {
          // Убираем пользователя из списка
          return prev.filter(user => user.id !== data.user_id);
        }
        return prev;
      });
    };

    // Подписываемся на события
    websocketService.on('online_users', handleOnlineUsers);
    websocketService.on('user_status', handleUserStatus);

    // Запрашиваем список при подключении
    if (websocketService.isConnected()) {
      fetchOnlineUsers();
    }

    // Периодически обновляем список
    const interval = setInterval(fetchOnlineUsers, 30000); // каждые 30 сек

    return () => {
      websocketService.off('online_users', handleOnlineUsers);
      websocketService.off('user_status', handleUserStatus);
      clearInterval(interval);
    };
  }, []);

  if (!isVisible || onlineUsers.length === 0) {
    return null;
  }

  return (
    <div className="online-users-list">
      <h4>🟢 Онлайн ({onlineUsers.length})</h4>
      {onlineUsers.map((user) => (
        <div key={user.id} className="online-user-item">
          <span className="online-badge"></span>
          <span className="user-name">{user.username}</span>
        </div>
      ))}
    </div>
  );
};

export default OnlineUsers;
