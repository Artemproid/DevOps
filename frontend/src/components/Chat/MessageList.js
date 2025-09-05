import React from 'react';
import ModernMessageFactory from './ModernMessageFactory';

function MessageList({ messages, currentUser }) {
  return (
    <div className="messages-list">
      {messages.map((message) => (
        <ModernMessageFactory 
          key={message.id}
          message={message}
          currentUser={currentUser}
        />
      ))}
    </div>
  );
}

export default MessageList; 