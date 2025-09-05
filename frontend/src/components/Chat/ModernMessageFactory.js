import React from 'react';
import { Badge, Card, Row, Col } from 'react-bootstrap';
import './ModernMessages.css';

/**
 * 🎨 Современная фабрика сообщений с аватарками и красивым дизайном
 */

// Типы сообщений
export const MessageType = {
  REGULAR: "regular",
  ASCII_ART: "ascii_art", 
  PIRATE: "pirate",
  SYSTEM: "system",
  KNIGHT: "knight",
  ROBOT: "robot"
};

/**
 * 🖼️ Генератор аватарок
 */
const getAvatarUrl = (username, userId) => {
  // Используем DiceBear API для генерации аватарок
  const styles = ['avataaars', 'bottts', 'identicon', 'initials', 'pixel-art'];
  const style = styles[userId % styles.length];
  return `https://api.dicebear.com/7.x/${style}/svg?seed=${username}&size=40`;
};

/**
 * 🎭 Получение иконки типа сообщения
 */
const getTypeIcon = (messageType) => {
  switch (messageType) {
    case MessageType.ASCII_ART:
      return { icon: '🎨', color: '#6c757d', label: 'ASCII Арт' };
    case MessageType.PIRATE:
      return { icon: '🏴‍☠️', color: '#fd7e14', label: 'Пиратское' };
    case MessageType.SYSTEM:
      return { icon: '🤖', color: '#17a2b8', label: 'Система' };
    case MessageType.KNIGHT:
      return { icon: '⚔️', color: '#6610f2', label: 'Рыцарское' };
    case MessageType.ROBOT:
      return { icon: '🔧', color: '#6c757d', label: 'Роботическое' };
    default:
      return { icon: '💬', color: '#007bff', label: 'Обычное' };
  }
};

/**
 * 🧠 Умное определение типа сообщения
 */
const detectMessageType = (content) => {
  // ASCII арт - принудительное определение
  if (content.includes('___') || 
      content.includes('\\') || 
      content.includes('//') ||
      /[_\/\\|]{4,}/.test(content) ||
      /\n.*[_\/\\|].*\n/.test(content)) {
    return MessageType.ASCII_ART;
  }
  
  const contentLower = content.toLowerCase().trim();
  
  // Системные сообщения
  if (contentLower.startsWith('🤖') || contentLower.startsWith('система:')) {
    return MessageType.SYSTEM;
  }
  
  // Пиратские сообщения
  const pirateWords = ['arr', 'ahoy', 'матей', 'корабль', 'сокровище', 'пират'];
  if (pirateWords.some(word => contentLower.includes(word))) {
    return MessageType.PIRATE;
  }
  
  return MessageType.REGULAR;
};

/**
 * ⏰ Форматирование времени
 */
const formatTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString('ru-RU', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

/**
 * 🏗️ Компонент заголовка сообщения
 */
const MessageHeader = ({ message, isMyMessage, messageType }) => {
  const typeInfo = getTypeIcon(messageType);
  
  return (
    <div className="modern-message-header">
      <div className="d-flex align-items-center gap-2">
        {/* Аватарка */}
        {!isMyMessage && (
          <img 
            src={getAvatarUrl(message.user?.username, message.user_id)}
            alt="Avatar"
            className="message-avatar"
            onError={(e) => {
              e.target.src = `https://ui-avatars.com/api/?name=${message.user?.username}&size=40&background=random`;
            }}
          />
        )}
        
        {/* Информация о пользователе */}
        <div className="flex-grow-1">
          <div className="d-flex align-items-center gap-2">
            <strong 
              className="username"
              style={messageType === MessageType.ASCII_ART ? { color: '#00ff00' } : {}}
            >
              {isMyMessage ? 'Вы' : message.user?.username || 'Пользователь'}
            </strong>
            
            {/* Бейдж типа сообщения */}
            <Badge 
              bg={messageType === MessageType.ASCII_ART ? "dark" : "light"}
              text={messageType === MessageType.ASCII_ART ? "light" : "dark"}
              className="type-badge"
              style={{ 
                fontSize: '10px',
                color: messageType === MessageType.ASCII_ART ? '#00ff00' : undefined
              }}
            >
              {typeInfo.icon} {typeInfo.label}
            </Badge>
          </div>
          
          <small 
            className="text-muted message-time"
            style={messageType === MessageType.ASCII_ART ? { color: '#00cc00' } : {}}
          >
            {formatTime(message.created_at)}
          </small>
        </div>
        
        {/* Аватарка для своих сообщений */}
        {isMyMessage && (
          <img 
            src={getAvatarUrl('Вы', message.user_id)}
            alt="Avatar"
            className="message-avatar"
          />
        )}
      </div>
    </div>
  );
};

/**
 * 📝 Компонент содержимого сообщения
 */
const MessageContent = ({ message, messageType }) => {
  const getContentComponent = () => {
    switch (messageType) {
      case MessageType.ASCII_ART:
        // DEBUG: логируем что приходит
        console.log('🎨 ASCII Content:', {
          content: message.content,
          length: message.content.length,
          hasNewlines: message.content.includes('\n'),
          lines: message.content.split('\n').length
        });
        
        return (
          <div 
            className="ascii-content"
            style={{
              background: '#000',
              borderRadius: '8px',
              padding: '12px',
              marginTop: '8px',
              border: '1px solid #333'
            }}
          >
            <div 
              className="ascii-text"
              style={{
                fontFamily: "'Courier New', 'Lucida Console', monospace",
                fontSize: '12px',
                lineHeight: '1.3',
                color: '#00ff00',
                margin: '0',
                whiteSpace: 'pre',
                overflowX: 'auto',
                textShadow: '0 0 5px rgba(0,255,0,0.5)',
                display: 'block',
                width: '100%'
              }}
            >
              {message.content}
            </div>
          </div>
        );
        
      case MessageType.SYSTEM:
        return (
          <div className="system-content">
            <em>{message.content}</em>
          </div>
        );
        
      case MessageType.PIRATE:
        return (
          <div className="pirate-content">
            <span className="pirate-text">{message.content}</span>
          </div>
        );
        
      case MessageType.KNIGHT:
        return (
          <div className="knight-content">
            <em className="knight-text">{message.content}</em>
          </div>
        );
        
      case MessageType.ROBOT:
        return (
          <div className="robot-content">
            <span className="robot-text">{message.content.toUpperCase()}</span>
          </div>
        );
        
      default:
        return (
          <div className="regular-content">
            {message.content}
          </div>
        );
    }
  };
  
  return (
    <div className="modern-message-content">
      {getContentComponent()}
    </div>
  );
};

/**
 * 🏭 Главная современная фабрика сообщений
 */
export const ModernMessageFactory = ({ message, currentUser }) => {
  const isMyMessage = message.user_id === currentUser?.id;
  
  // ВРЕМЕННО: Принудительно делаем все сообщения с подчеркиваниями ASCII
  let messageType = message.message_type || detectMessageType(message.content);
  if (message.content.includes('___') || message.content.includes('\\') || message.content.includes('//')) {
    messageType = MessageType.ASCII_ART;
  }
  
  const getCardClasses = () => {
    const baseClass = 'modern-message-card';
    const alignClass = isMyMessage ? 'my-message' : 'other-message';
    const typeClass = `message-type-${messageType}`;
    
    return `${baseClass} ${alignClass} ${typeClass}`;
  };

  const getCardStyle = () => {
    if (messageType === MessageType.ASCII_ART) {
      return {
        background: '#1a1a1a',
        color: '#00ff00',
        border: '2px solid #333',
        maxWidth: '90%'
      };
    }
    return {};
  };
  
  return (
    <div className={`modern-message-wrapper ${isMyMessage ? 'justify-content-end' : 'justify-content-start'}`}>
      <Card className={getCardClasses()} style={getCardStyle()}>
        <Card.Body className="modern-message-body">
          <MessageHeader 
            message={message} 
            isMyMessage={isMyMessage} 
            messageType={messageType}
          />
          <MessageContent 
            message={message} 
            messageType={messageType}
          />
        </Card.Body>
      </Card>
    </div>
  );
};

export default ModernMessageFactory;
