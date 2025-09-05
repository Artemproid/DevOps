/**
 * 🏴‍☠️ ПРЕДПРОСМОТР ПИРАТСКОГО ТЕКСТА
 * 
 * Показывает как будет выглядеть сообщение в пиратском стиле
 */

import React, { useState, useEffect } from 'react';
import { Card, Badge, Spinner } from 'react-bootstrap';

function PiratePreview({ originalText, transformFunction, isVisible = true }) {
  const [pirateText, setPirateText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Трансформируем текст при изменении
  useEffect(() => {
    if (!originalText || !originalText.trim() || !transformFunction || !isVisible) {
      setPirateText('');
      return;
    }

    const transformText = async () => {
      setIsLoading(true);
      setError('');
      
      try {
        const result = await transformFunction(originalText);
        setPirateText(result.pirate_text || result.styled || '');
      } catch (err) {
        console.error('Ошибка трансформации текста:', err);
        setError('Ошибка стилизации');
        setPirateText('');
      } finally {
        setIsLoading(false);
      }
    };

    // Добавляем небольшую задержку чтобы не спамить API
    const timeoutId = setTimeout(transformText, 300);
    
    return () => clearTimeout(timeoutId);
  }, [originalText, transformFunction, isVisible]);

  if (!isVisible || (!originalText && !pirateText)) {
    return null;
  }

  return (
    <Card className="pirate-preview mt-2" style={{ backgroundColor: '#fef7e0', border: '1px solid #ffa500' }}>
      <Card.Body className="py-2">
        <div className="d-flex align-items-start gap-2">
          <Badge bg="warning" text="dark">🏴‍☠️ Пиратский стиль</Badge>
          <div className="flex-grow-1">
            {isLoading ? (
              <div className="d-flex align-items-center gap-2">
                <Spinner size="sm" />
                <small className="text-muted">Стилизация...</small>
              </div>
            ) : error ? (
              <small className="text-danger">{error}</small>
            ) : pirateText ? (
              <div className="pirate-text" style={{ fontStyle: 'italic', color: '#8b4513' }}>
                "{pirateText}"
              </div>
            ) : (
              <small className="text-muted">Введите текст для предпросмотра...</small>
            )}
          </div>
        </div>
      </Card.Body>
    </Card>
  );
}

export default PiratePreview;
