import React from 'react';
import { Badge } from 'react-bootstrap';

/**
 * 🏭 Фабрика компонентов сообщений
 */

// Типы сообщений (синхронизировано с бэкендом)
export const MessageType = {
  REGULAR: "normal",
  ASCII_ART: "ascii_art", 
  SYSTEM: "system"
};

/**
 * Определяет тип сообщения на основе содержимого
 */
export const detectMessageType = (content) => {
  // ASCII арт - более агрессивное определение
  const asciiPatterns = [
    /[╔╗╚╝═║┌┐└┘─│]/g,  // Рамки
    /[▄▀█▌▐]/g,         // Блоки
    /[/\\|_-]{3,}/g,   // Понижен порог с 5 до 3
    /\s+[_/\\|]{2,}/g, // ASCII символы с пробелами
  ];
  
  // Проверяем на ASCII символы
  const hasASCIIChars = asciiPatterns.some(pattern => {
    const matches = content.match(pattern);
    return matches && matches.length >= 1; // Понижен порог
  });
  
  // Проверяем многострочность
  const lines = content.split('\n');
  const hasMultipleLines = lines.length >= 2; // Понижен порог с 3 до 2
  
  // Проверяем ASCII строки
  const hasASCIILines = lines.some(line => {
    const trimmed = line.trim();
    // Если строка содержит много ASCII символов
    const asciiSymbols = (trimmed.match(/[_/\\|+\-=<>(){}[\]]/g) || []).length;
    return asciiSymbols >= 3 && trimmed.length > 3; // Понижен порог
  });
  
  // Если содержит характерные ASCII последовательности
  const hasASCIISequences = /[_/\\|-]{4,}/.test(content) || 
                           /\s+[_/\\|]{2,}\s+/.test(content);
  
  if (hasASCIIChars || hasASCIISequences || (hasMultipleLines && hasASCIILines)) {
    return MessageType.ASCII_ART;
  }
  
  // Системные сообщения
  const contentLower = content.toLowerCase().trim();
  if (contentLower.startsWith('🤖') || contentLower.startsWith('система:')) {
    return MessageType.SYSTEM;
  }
  
  return MessageType.REGULAR;
};

/**
 * Базовый компонент сообщения
 */
const BaseMessage = ({ message, isMyMessage, children }) => {
  const messageType = message.message_type || detectMessageType(message.content);
  
  // Определяем CSS классы в зависимости от типа
  const getMessageClasses = () => {
    const baseClasses = `message-item ${isMyMessage ? 'my-message' : 'other-message'}`;
    
    switch (messageType) {
      case MessageType.ASCII_ART:
        return `${baseClasses} ascii-art`;
      case MessageType.SYSTEM:
        return `${baseClasses} system-message`;
      default:
        return baseClasses;
    }
  };
  
  return (
    <div className={getMessageClasses()}>
      {children}
    </div>
  );
};

/**
 * Компонент заголовка сообщения с типом
 */
const MessageHeader = ({ message, isMyMessage }) => {
  const messageType = message.message_type || detectMessageType(message.content);
  
  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('ru-RU', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };
  
  const getTypeBadge = () => {
    switch (messageType) {
      case MessageType.ASCII_ART:
        return <Badge bg="secondary" style={{fontSize: '10px'}}>🎨 ASCII</Badge>;
      case MessageType.SYSTEM:
        return <Badge bg="info" style={{fontSize: '10px'}}>🤖 Система</Badge>;
      default:
        return null;
    }
  };
  
  return (
    <div className="message-header">
      <strong>
        {isMyMessage ? 'Вы' : message.user?.username || 'Пользователь'}
      </strong>
      <span className="message-time">
        {formatTime(message.created_at)}
      </span>
      {getTypeBadge() && (
        <span className="ms-2">
          {getTypeBadge()}
        </span>
      )}
    </div>
  );
};

/**
 * Компонент содержимого сообщения
 */
const MessageContent = ({ message }) => {
  const messageType = message.message_type || detectMessageType(message.content);
  
  // Принудительно определяем ASCII арт
  const isDefinitelyASCII = message.message_type === 'ascii_art' || 
                           message.content.includes('___') ||
                           message.content.includes('\\') ||
                           message.content.includes('//') ||
                           /[_/\\|]{4,}/.test(message.content);
  
  const getContentClasses = () => {
    // Принудительно применяем ASCII стили
    if (isDefinitelyASCII) {
      return 'message-content ascii-art-content';
    }
    
    switch (messageType) {
      case MessageType.ASCII_ART:
        return 'message-content ascii-art-content';
      case MessageType.SYSTEM:
        return 'message-content system-content';
      default:
        return 'message-content';
    }
  };
  
  return (
    <div className={getContentClasses()}>
      {message.content}
    </div>
  );
};

/**
 * 🏭 Главная фабрика сообщений
 */
export const MessageFactory = ({ message, currentUser }) => {
  const isMyMessage = message.user_id === currentUser?.id;
  
  return (
    <BaseMessage message={message} isMyMessage={isMyMessage}>
      <MessageHeader message={message} isMyMessage={isMyMessage} />
      <MessageContent message={message} />
    </BaseMessage>
  );
};

export default MessageFactory;
