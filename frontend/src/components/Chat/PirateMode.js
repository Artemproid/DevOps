/**
 * 🏴‍☠️ КОМПОНЕНТ ПИРАТСКОГО РЕЖИМА
 * 
 * Кнопка для включения/выключения пиратской стилизации
 */

import React, { useState, useEffect } from 'react';
import { Button, Spinner, Tooltip, OverlayTrigger, Alert } from 'react-bootstrap';
import pirateService from '../../services/pirate.service';

function PirateMode({ onTextTransform, className = '', isPremium = false }) {
  const [isActive, setIsActive] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [apiAvailable, setApiAvailable] = useState(true);
  const [lastExclamation, setLastExclamation] = useState('');
  const [premiumError, setPremiumError] = useState('');

  // Проверяем доступность API при монтировании
  useEffect(() => {
    checkApiAvailability();
  }, []);

  const checkApiAvailability = async () => {
    const available = await pirateService.isApiAvailable();
    setApiAvailable(available);
  };

  const handleToggle = async () => {
    if (isActive) {
      // Выключаем пиратский режим
      setIsActive(false);
      onTextTransform(null);
      setPremiumError('');
    } else {
      // Проверяем премиум статус перед включением
      if (!isPremium) {
        setPremiumError('🚫 Пиратский режим доступен только для Premium пользователей!');
        return;
      }

      // Включаем пиратский режим
      setIsLoading(true);
      setPremiumError('');
      try {
        // Получаем пиратское приветствие
        const exclamation = await pirateService.getExclamation();
        setLastExclamation(exclamation);
        
        setIsActive(true);
        onTextTransform(pirateService.piratifyText.bind(pirateService));
        
        // Показываем уведомление
        console.log(`🏴‍☠️ Пиратский режим активирован! ${exclamation}`);
        
      } catch (error) {
        console.error('Ошибка активации пиратского режима:', error);
        
        // Если ошибка 403 - проблема с премиум статусом
        if (error.response?.status === 403) {
          setPremiumError(error.response.data.detail || 'Нужна премиум подписка');
          setIsActive(false);
          onTextTransform(null);
        } else {
          // Другие ошибки - включаем с локальным fallback
          setIsActive(true);
          onTextTransform(pirateService.piratifyText.bind(pirateService));
        }
      } finally {
        setIsLoading(false);
      }
    }
  };

  const buttonVariant = isActive ? 'warning' : (isPremium ? 'outline-warning' : 'outline-secondary');
  const buttonText = isActive ? '🏴‍☠️ Пиратский режим ВКЛ' : (isPremium ? '🏴‍☠️ Пиратский режим' : '🔒 Пиратский режим (Premium)');

  const tooltip = (
    <Tooltip id="pirate-tooltip">
      {isActive 
        ? 'Выключить пиратскую стилизацию сообщений' 
        : 'Включить пиратскую стилизацию сообщений'
      }
      {!apiAvailable && (
        <div><small>⚠️ API недоступен, используется локальная стилизация</small></div>
      )}
      {lastExclamation && (
        <div><small>💬 {lastExclamation}</small></div>
      )}
    </Tooltip>
  );

  return (
    <div className={`pirate-mode-container ${className}`}>
      <OverlayTrigger placement="top" overlay={tooltip}>
        <Button
          variant={buttonVariant}
          size="sm"
          onClick={handleToggle}
          disabled={isLoading}
          className="d-flex align-items-center gap-1"
        >
          {isLoading ? (
            <>
              <Spinner size="sm" />
              <span>Загрузка...</span>
            </>
          ) : (
            <>
              <span>{buttonText}</span>
              {isActive && <span className="badge bg-light text-dark ms-1">ON</span>}
            </>
          )}
        </Button>
      </OverlayTrigger>
      
      {!apiAvailable && (
        <Alert variant="warning" className="mt-2 p-2" style={{ fontSize: '0.8rem' }}>
          <small>
            ⚠️ Пиратский API недоступен. Используется упрощенная стилизация.
          </small>
        </Alert>
      )}
      
      {premiumError && (
        <Alert variant="danger" className="mt-2 p-2" style={{ fontSize: '0.8rem' }}>
          <small>
            {premiumError}
          </small>
        </Alert>
      )}
    </div>
  );
}

export default PirateMode;
