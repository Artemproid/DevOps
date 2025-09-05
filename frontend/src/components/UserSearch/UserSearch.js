import React, { useState, useEffect, useRef } from 'react';
import { Form, ListGroup, Card, Badge, Spinner, Alert } from 'react-bootstrap';
import userService from '../../services/user.service';
import websocketService from '../../services/websocket.service';
import './UserSearch.css';

function UserSearch({ onUserSelect }) {
  const [query, setQuery] = useState('');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showResults, setShowResults] = useState(false);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const searchRef = useRef(null);
  const timeoutRef = useRef(null);

  // Debounced поиск
  useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    if (query.trim().length >= 2) {
      timeoutRef.current = setTimeout(() => {
        searchUsers(query.trim());
      }, 300);
    } else {
      setUsers([]);
      setShowResults(false);
    }

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [query]);

  // Отслеживаем онлайн пользователей
  useEffect(() => {
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

    websocketService.on('online_users', handleOnlineUsers);
    websocketService.on('user_status', handleUserStatus);

    // Запрашиваем список при загрузке
    if (websocketService.isConnected()) {
      websocketService.getOnlineUsers();
    }

    return () => {
      websocketService.off('online_users', handleOnlineUsers);
      websocketService.off('user_status', handleUserStatus);
    };
  }, []);

  // Закрытие результатов при клике вне компонента
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const searchUsers = async (searchQuery) => {
    try {
      setLoading(true);
      setError('');
      const results = await userService.searchUsers(searchQuery);
      setUsers(results);
      setShowResults(true);
    } catch (err) {
      console.error('Error searching users:', err);
      setError('Ошибка при поиске пользователей');
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const handleUserClick = (user) => {
    setQuery('');
    setUsers([]);
    setShowResults(false);
    if (onUserSelect) {
      onUserSelect(user);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    if (value.trim().length === 0) {
      setShowResults(false);
    }
  };

  const handleInputFocus = () => {
    if (users.length > 0) {
      setShowResults(true);
    }
  };

  return (
    <div className="user-search" ref={searchRef}>
      <Form.Group className="mb-3">
        <Form.Control
          type="text"
          placeholder="Поиск пользователей..."
          value={query}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          className="user-search-input"
        />
      </Form.Group>

      {showResults && (
        <Card className="user-search-results">
          {loading && (
            <div className="text-center p-3">
              <Spinner animation="border" size="sm" />
              <span className="ms-2">Поиск...</span>
            </div>
          )}

          {error && (
            <Alert variant="danger" className="m-2">
              {error}
            </Alert>
          )}

          {!loading && users.length === 0 && query.trim().length >= 2 && (
            <div className="text-center p-3 text-muted">
              Пользователи не найдены
            </div>
          )}

          {!loading && users.length > 0 && (
            <ListGroup variant="flush">
              {users.map((user) => (
                <ListGroup.Item
                  key={user.id}
                  action
                  onClick={() => handleUserClick(user)}
                  className="user-search-item"
                >
                  <div className="d-flex justify-content-between align-items-center">
                    <div>
                      <div className="fw-bold">
                        {user.username}
                        {onlineUsers.find(ou => ou.id === user.id) ? (
                          <span className="online-badge" title="Онлайн"></span>
                        ) : (
                          <span className="offline-badge" title="Оффлайн"></span>
                        )}
                      </div>
                      <small className="text-muted">{user.email}</small>
                    </div>
                    <div>
                      {onlineUsers.find(ou => ou.id === user.id) ? (
                        <Badge bg="success">🟢 Онлайн</Badge>
                      ) : user.is_active ? (
                        <Badge bg="warning">🟡 Оффлайн</Badge>
                      ) : (
                        <Badge bg="secondary">Неактивен</Badge>
                      )}
                    </div>
                  </div>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
        </Card>
      )}
    </div>
  );
}

export default UserSearch;
