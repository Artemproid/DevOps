import React, { useState, useEffect } from 'react';
import { Card, Button, Form, Row, Col, Alert, Badge, Spinner } from 'react-bootstrap';
import axios from '../../utils/axios';

function ASCIIArtGenerator({ isPremium }) {
  const [text, setText] = useState('');
  const [selectedFont, setSelectedFont] = useState('slant');
  const [asciiArt, setAsciiArt] = useState('');
  const [availableFonts, setAvailableFonts] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showDemo, setShowDemo] = useState(false);
  const [showASCII, setShowASCII] = useState(false);

  // Загружаем список шрифтов при монтировании
  useEffect(() => {
    if (isPremium) {
      loadAvailableFonts();
    } else {
      loadDemo();
    }
  }, [isPremium]);

  const loadAvailableFonts = async () => {
    try {
      const response = await axios.get('/ascii-generator/fonts');
      setAvailableFonts(response.data.fonts);
      
      // Устанавливаем первый доступный шрифт
      const firstFont = Object.keys(response.data.fonts)[0];
      if (firstFont) {
        setSelectedFont(firstFont);
      }
    } catch (error) {
      console.error('Ошибка загрузки шрифтов:', error);
      setError('Не удалось загрузить список шрифтов');
    }
  };

  const loadDemo = async () => {
    try {
      const response = await axios.get('/ascii-generator/demo');
      setAsciiArt(response.data.ascii_art);
      setShowDemo(true);
    } catch (error) {
      console.error('Ошибка загрузки демо:', error);
    }
  };

  const generateArt = async () => {
    if (!text.trim()) {
      setError('Введите текст для генерации');
      return;
    }

    if (!isPremium) {
      setError('ASCII арт доступен только для Premium пользователей!');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/ascii-generator/generate', {
        text: text.trim(),
        font: selectedFont
      });

      setAsciiArt(response.data.ascii_art);
      
    } catch (error) {
      console.error('Ошибка генерации ASCII арт:', error);
      setError(error.response?.data?.detail || 'Ошибка генерации ASCII арт');
    } finally {
      setLoading(false);
    }
  };

  const handleTextChange = (e) => {
    const value = e.target.value;
    if (value.length <= 50) { // Ограничиваем длину
      setText(value);
      setError('');
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(asciiArt);
      // Можно добавить toast уведомление
    } catch (error) {
      console.error('Ошибка копирования:', error);
    }
  };

  const sendToChat = () => {
    if (asciiArt && typeof window !== 'undefined') {
      // Вместо вставки в input, напрямую отправляем через API
      // Находим компонент чата и вызываем функцию отправки
      const sendButton = document.querySelector('button[type="submit"]');
      if (sendButton) {
        // Создаем кастомное событие с ASCII данными
        const customEvent = new CustomEvent('sendASCII', {
          detail: { asciiArt, messageType: 'ascii_art' }
        });
        document.dispatchEvent(customEvent);
      }
    }
  };

  return (
    <Card className="mb-2" style={{ 
      background: isPremium ? 
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 
        'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
    }}>
      <Card.Body className="py-2 px-3">
        <div className="d-flex align-items-center justify-content-between mb-2">
          <span className="fw-bold text-white small">
            🎨 ASCII Арт 
            {isPremium ? (
              <Badge bg="success" className="ms-1" style={{fontSize: '10px'}}>ON</Badge>
            ) : (
              <Badge bg="warning" className="ms-1" style={{fontSize: '10px'}}>Demo</Badge>
            )}
          </span>
          <Button
            variant="outline-light"
            size="sm"
            onClick={() => setShowASCII(!showASCII)}
            style={{fontSize: '11px', padding: '2px 8px'}}
          >
            {showASCII ? '▼' : '▶'}
          </Button>
        </div>

        {showASCII && (
          <>
            {error && (
              <Alert variant="danger" className="mb-2">
                {error}
              </Alert>
            )}

            {/* Компактная форма в одну строку */}
        <Row className="mb-3">
          <Col md={4}>
            <Form.Group>
              <Form.Label className="text-white small">
                <strong>Текст:</strong>
              </Form.Label>
              <Form.Control
                type="text"
                placeholder="Введите текст..."
                value={text}
                onChange={handleTextChange}
                disabled={!isPremium}
                maxLength={50}
                size="sm"
              />
              <Form.Text className="text-light small">
                {text.length}/50
              </Form.Text>
            </Form.Group>
          </Col>

          <Col md={3}>
            {isPremium && Object.keys(availableFonts).length > 0 && (
              <Form.Group>
                <Form.Label className="text-white small">
                  <strong>Шрифт:</strong>
                </Form.Label>
                <Form.Select
                  value={selectedFont}
                  onChange={(e) => setSelectedFont(e.target.value)}
                  size="sm"
                >
                  {Object.keys(availableFonts).map(font => (
                    <option key={font} value={font}>
                      {font}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            )}
          </Col>

          <Col md={5} className="d-flex align-items-end">
            <div className="d-flex gap-2 w-100">
              <Button
                variant={isPremium ? "light" : "outline-light"}
                onClick={generateArt}
                disabled={loading || !isPremium || !text.trim()}
                size="sm"
                className="flex-grow-1"
              >
                {loading ? (
                  <>
                    <Spinner size="sm" className="me-1" />
                    Генерирую...
                  </>
                ) : (
                  '🎨 Создать'
                )}
              </Button>

              {asciiArt && (
                <>
                  <Button
                    variant="outline-light"
                    size="sm"
                    onClick={sendToChat}
                    title="Отправить в чат"
                    className="me-1"
                  >
                    💬
                  </Button>
                  <Button
                    variant="outline-light"
                    size="sm"
                    onClick={copyToClipboard}
                    title="Скопировать в буфер обмена"
                  >
                    📋
                  </Button>
                </>
              )}
            </div>
          </Col>
        </Row>

        {/* Превью шрифта - только если выбран */}
        {isPremium && selectedFont && availableFonts[selectedFont] && (
          <Row className="mb-3">
            <Col>
              <Form.Label className="text-white small">
                <strong>Превью шрифта "{selectedFont}":</strong>
              </Form.Label>
              <div 
                style={{
                  background: 'rgba(255,255,255,0.1)',
                  padding: '8px',
                  borderRadius: '4px',
                  fontFamily: 'monospace',
                  fontSize: '11px',
                  whiteSpace: 'pre',
                  color: 'white',
                  overflow: 'auto',
                  maxHeight: '80px'
                }}
              >
                {availableFonts[selectedFont]}
              </div>
            </Col>
          </Row>
        )}

        {/* Результат ASCII арт */}
        {asciiArt && (
          <div className="mt-3">
            <Form.Label className="text-white">
              <strong>
                {showDemo ? '🎯 Демо результат:' : '✨ Ваш ASCII арт:'}
              </strong>
            </Form.Label>
            <div 
              style={{
                background: 'rgba(0,0,0,0.4)',
                padding: '12px',
                borderRadius: '6px',
                fontFamily: 'monospace',
                fontSize: '11px',
                whiteSpace: 'pre',
                color: showDemo ? '#ffd700' : '#ffffff',
                overflow: 'auto',
                maxHeight: '200px',
                border: '1px solid rgba(255,255,255,0.3)'
              }}
            >
              {asciiArt}
            </div>
            {showDemo && (
              <small className="text-light d-block mt-2">
                💡 Получите Premium для создания собственных ASCII артов!
              </small>
            )}
          </div>
        )}

        {!isPremium && (
          <div className="mt-3 p-3" style={{ 
            background: 'rgba(255,255,255,0.1)', 
            borderRadius: '8px',
            border: '2px dashed #ffc107'
          }}>
            <h6 className="text-white">🎯 Что даёт ASCII Арт Premium:</h6>
            <ul className="mb-0 text-light">
              <li>🎨 <strong>10+ уникальных шрифтов</strong> для ASCII арт</li>
              <li>⚡ <strong>Мгновенная генерация</strong> любого текста</li>
              <li>📋 <strong>Копирование в буфер</strong> одним кликом</li>
              <li>✨ <strong>Превью шрифтов</strong> перед созданием</li>
            </ul>
          </div>
        )}
          </>
        )}
      </Card.Body>
    </Card>
  );
}

export default ASCIIArtGenerator;
