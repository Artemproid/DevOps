import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import ChatList from './ChatList';
import ChatBox from './ChatBox';
import './Chat.css';

function ChatLayout() {
  const [showSidebar, setShowSidebar] = useState(true);

  return (
    <div className="chat-layout">
      {/* Кнопка toggle для мобильных */}
      <Button
        className="sidebar-toggle d-md-none"
        variant="outline-secondary"
        size="sm"
        onClick={() => setShowSidebar(!showSidebar)}
      >
        {showSidebar ? '×' : '☰'}
      </Button>

      {/* Боковая панель со списком чатов */}
      <div className={`sidebar ${showSidebar ? 'show' : ''}`}>
        <ChatList />
      </div>

      {/* Основной контент с чатом */}
      <div className={`main-content ${!showSidebar ? 'full-width' : ''}`}>
        <ChatBox />
      </div>
    </div>
  );
}

export default ChatLayout;
