import React from 'react';
import { ButtonGroup, Dropdown, DropdownButton } from 'react-bootstrap';
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
      case MessageType.SYSTEM:
        return '🤖';
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
      case MessageType.SYSTEM:
        return 'Системное';
      default:
        return 'Обычное';
    }
  };

  const availableTypes = [
    MessageType.REGULAR,
    MessageType.ASCII_ART,
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
        >
          <span className="d-flex align-items-center">
            <span className="me-2">{getTypeIcon(type)}</span>
            <span>{getTypeName(type)}</span>
          </span>
        </Dropdown.Item>
      ))}
    </DropdownButton>
  );
}

export default MessageTypeSelector;
