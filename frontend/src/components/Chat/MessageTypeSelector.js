import React, { useState } from 'react';
import { Button, ButtonGroup, Dropdown, DropdownButton } from 'react-bootstrap';
import { MessageType } from './MessageFactory';

/**
 * 🎭 Селектор типов сообщений
 */
function MessageTypeSelector({ selectedType, onTypeChange, isPremium }) {
  const getTypeIcon = (type) => {
    switch (type) {
      case MessageType.REGULAR:
        return '💬';
      case MessageType.ASCII_ART:
        return '🎨';
      case MessageType.PIRATE:
        return '🏴‍☠️';
      case MessageType.SYSTEM:
        return '🤖';
      case MessageType.KNIGHT:
        return '⚔️';
      case MessageType.ROBOT:
        return '🔧';
      default:
        return '💬';
    }
  };

  const getTypeName = (type) => {
    switch (type) {
      case MessageType.REGULAR:
        return 'Обычное';
      case MessageType.ASCII_ART:
        return 'ASCII Арт';
      case MessageType.PIRATE:
        return 'Пиратское';
      case MessageType.SYSTEM:
        return 'Системное';
      case MessageType.KNIGHT:
        return 'Рыцарское';
      case MessageType.ROBOT:
        return 'Роботическое';
      default:
        return 'Обычное';
    }
  };

  const isPremiumType = (type) => {
    return [MessageType.PIRATE, MessageType.KNIGHT, MessageType.ROBOT].includes(type);
  };

  const availableTypes = [
    MessageType.REGULAR,
    MessageType.ASCII_ART,
    ...(isPremium ? [MessageType.PIRATE, MessageType.KNIGHT, MessageType.ROBOT] : []),
    MessageType.SYSTEM
  ];

  return (
    <DropdownButton
      as={ButtonGroup}
      id="message-type-dropdown"
      title={
        <span>
          {getTypeIcon(selectedType)} {getTypeName(selectedType)}
        </span>
      }
      variant={selectedType === MessageType.REGULAR ? "outline-secondary" : "outline-primary"}
      size="sm"
      className="me-2"
    >
      {availableTypes.map((type) => (
        <Dropdown.Item
          key={type}
          active={selectedType === type}
          onClick={() => onTypeChange(type)}
          disabled={!isPremium && isPremiumType(type)}
        >
          <span className="d-flex align-items-center">
            <span className="me-2">{getTypeIcon(type)}</span>
            <span>{getTypeName(type)}</span>
            {!isPremium && isPremiumType(type) && (
              <span className="ms-auto">
                <small className="text-muted">🔒 Premium</small>
              </span>
            )}
          </span>
        </Dropdown.Item>
      ))}
    </DropdownButton>
  );
}

export default MessageTypeSelector;
