import React, { useState, useEffect, useRef } from 'react';
import { Form, Button, Card, ButtonGroup, Modal, Dropdown } from 'react-bootstrap';
import MessageList from './MessageList';
import asciiService from '../../services/ascii.service';
import './Chat.css';

function ChatBox() {
  const [messages, setMessages] = useState(() => {
    // Загружаем сообщения из localStorage при инициализации
    const savedMessages = localStorage.getItem('chatMessages');
    return savedMessages ? JSON.parse(savedMessages) : [{
      id: 1,
      content: 'Привет! Я бот. Выберите команду, чтобы начать диалог.',
      created_at: new Date().toISOString(),
      isBot: true
    }];
  });
  
  const [newMessage, setNewMessage] = useState('');
  const [awaitingUserInput, setAwaitingUserInput] = useState(false);
  const [currentCommand, setCurrentCommand] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showStyleModal, setShowStyleModal] = useState(false);
  const [selectedStyle, setSelectedStyle] = useState('extended');
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);
  
  // Доступные стили
  const styles = asciiService.getAvailableStyles();

  // Сохраняем сообщения в localStorage при их изменении
  useEffect(() => {
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  const handleCommand = (command) => {
    setCurrentCommand(command);
    setAwaitingUserInput(true);
    
    let promptMessage;
    if (command === 'Команда 1') {
      promptMessage = 'Напишите текст:';
    } else if (command === 'Команда 2') {
      promptMessage = 'Загрузите изображение для преобразования в ASCII-арт:';
      fileInputRef.current?.click();
      return;
    } else if (command === 'Команда 3') {
      // Очистка чата
      const newMessages = [{
        id: Date.now(),
        content: 'Чат очищен. Выберите команду, чтобы начать диалог.',
        created_at: new Date().toISOString(),
        isBot: true
      }];
      setMessages(newMessages);
      localStorage.setItem('chatMessages', JSON.stringify(newMessages));
      setAwaitingUserInput(false);
      setCurrentCommand(null);
      return;
    }

    const newBotMessage = {
      id: Date.now(),
      content: promptMessage,
      created_at: new Date().toISOString(),
      isBot: true
    };

    setMessages(prev => [...prev, newBotMessage]);
  };

  const handleFileChange = async (event) => {
    console.log('File input event triggered');
    const file = event.target.files[0];
    if (!file) {
      console.error('No file selected!');
      return;
    }

    console.log('File selected:', file);
    console.log('File name:', file.name);
    console.log('File size:', file.size);
    console.log('File type:', file.type);
    
    // Сохраняем файл и показываем модальное окно для выбора стиля
    setSelectedFile(file);
    setShowStyleModal(true);
  };
  
  const handleStyleSelect = (styleValue) => {
    setSelectedStyle(styleValue);
  };
  
  const handleConvertWithStyle = async () => {
    // Закрываем модальное окно
    setShowStyleModal(false);
    
    if (!selectedFile) {
      console.error('No file selected!');
      return;
    }
    
    try {
      setIsProcessing(true);

      // Добавляем сообщение о загрузке файла
      const userMessage = {
        id: Date.now(),
        content: `Загружено изображение: ${selectedFile.name} (стиль: ${styles.find(s => s.value === selectedStyle)?.label})`,
        created_at: new Date().toISOString(),
        isBot: false
      };
      setMessages(prev => [...prev, userMessage]);

      console.log('Starting ASCII conversion request with style:', selectedStyle);
      // Конвертируем изображение с выбранным стилем
      const result = await asciiService.convertToAscii(selectedFile, selectedStyle);
      console.log('ASCII conversion successful:', result);

      // Добавляем ASCII-арт в чат
      const botResponse = {
        id: Date.now() + 1,
        content: result.ascii_art,
        created_at: new Date().toISOString(),
        isBot: true,
        isAsciiArt: true
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        content: 'Не удалось обработать изображение. Попробуйте другое.',
        created_at: new Date().toISOString(),
        isBot: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
      setAwaitingUserInput(false);
      setCurrentCommand(null);
      setSelectedFile(null);
      // Сбрасываем input file
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!newMessage.trim()) return;
    
    // Добавляем сообщение пользователя
    const userMessage = {
      id: Date.now(),
      content: newMessage,
      created_at: new Date().toISOString(),
      isBot: false
    };

    // Создаем ответ бота в зависимости от команды
    let botResponse;
    if (currentCommand === 'Команда 1') {
      botResponse = {
        id: Date.now() + 1,
        content: newMessage, // эхо введенного текста
        created_at: new Date().toISOString(),
        isBot: true
      };
    }

    setMessages(prev => [...prev, userMessage, botResponse]);
    setNewMessage('');
    setAwaitingUserInput(false);
    setCurrentCommand(null);
  };

  return (
    <>
      <Card className="chat-card">
        <Card.Header className="chat-header">
          <h2 className="text-center m-0">Чат-бот</h2>
        </Card.Header>
        
        <Card.Body className="chat-body p-0">
          <div className="chat-messages-container">
            <MessageList messages={messages} />
          </div>
          
          <div className="command-buttons">
            <ButtonGroup>
              <Button 
                variant="outline-primary" 
                onClick={() => handleCommand('Команда 1')}
                disabled={isProcessing}
              >
                Эхо
              </Button>
              <Button 
                variant="outline-primary" 
                onClick={() => handleCommand('Команда 2')}
                disabled={isProcessing}
              >
                ASCII-арт
              </Button>
              <Button 
                variant="outline-danger" 
                onClick={() => handleCommand('Команда 3')}
                disabled={isProcessing}
              >
                Очистить
              </Button>
            </ButtonGroup>
          </div>
          
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
            style={{ display: 'none' }}
          />
          
          <Form onSubmit={handleSubmit} className="message-form">
            <Form.Group className="message-input-group">
              <Form.Control
                className="message-input"
                type="text"
                placeholder={awaitingUserInput ? "Введите ваш ответ..." : "Сначала выберите команду..."}
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                disabled={!awaitingUserInput || isProcessing}
              />
              <Button 
                variant="primary" 
                type="submit" 
                className="send-button"
                disabled={!newMessage.trim() || !awaitingUserInput || isProcessing}
              >
                Отправить
              </Button>
            </Form.Group>
          </Form>
        </Card.Body>
      </Card>
      
      {/* Модальное окно для выбора стиля ASCII-арта */}
      <Modal show={showStyleModal} onHide={() => setShowStyleModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Выберите стиль ASCII-арта</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="mb-3">
            <Form.Label>Стиль преобразования:</Form.Label>
            <Form.Select 
              value={selectedStyle} 
              onChange={(e) => handleStyleSelect(e.target.value)}
            >
              {styles.map(style => (
                <option key={style.value} value={style.value}>
                  {style.label}
                </option>
              ))}
            </Form.Select>
          </div>
          <p className="text-muted">
            От выбранного стиля зависит набор символов, используемых для создания изображения.
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowStyleModal(false)}>
            Отмена
          </Button>
          <Button 
            variant="primary" 
            onClick={handleConvertWithStyle}
            disabled={isProcessing}
          >
            Конвертировать
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default ChatBox; 