import React, { useEffect, useState } from 'react';
import { Container, Card, Button, Alert, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import api from '../../utils/axios';

function PaymentSuccess() {
  const navigate = useNavigate();
  const [activating, setActivating] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Автоматически активируем премиум при загрузке страницы
    activatePremium();
    
    // Автоматический редирект через 5 секунд
    const timer = setTimeout(() => {
      navigate('/');
    }, 5000);

    return () => clearTimeout(timer);
  }, [navigate]);

  const activatePremium = async () => {
    try {
      setActivating(true);
      const response = await api.post('/payments/test-activate-premium');
      console.log('Premium activated:', response.data);
      setActivating(false);
    } catch (error) {
      console.error('Error activating premium:', error);
      setError('Ошибка активации премиума');
      setActivating(false);
    }
  };

  return (
    <Container className="mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <Card className="text-center" style={{ 
            background: 'linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)',
            border: '3px solid #ffa500'
          }}>
            <Card.Body className="p-5">
              <div className="mb-4">
                <div style={{ fontSize: '4rem' }}>🏴‍☠️</div>
                <h2 className="text-dark">Поздравляем!</h2>
              </div>
              
              {activating ? (
                <Alert variant="info" className="mb-4">
                  <div className="d-flex align-items-center">
                    <Spinner animation="border" size="sm" className="me-2" />
                    <div>
                      <h5>⚡ Активируем ваш премиум...</h5>
                      <p className="mb-0">Подождите, настраиваем пиратский режим!</p>
                    </div>
                  </div>
                </Alert>
              ) : error ? (
                <Alert variant="warning" className="mb-4">
                  <h5>⚠️ {error}</h5>
                  <p className="mb-0">
                    Оплата прошла, но возникла проблема с активацией. Свяжитесь с поддержкой.
                  </p>
                </Alert>
              ) : (
                <Alert variant="success" className="mb-4">
                  <h5>💳 Оплата прошла успешно!</h5>
                  <p className="mb-0">
                    Ваша премиум подписка активирована. Теперь вы можете использовать пиратский режим!
                  </p>
                </Alert>
              )}

              <div className="mb-4 p-3" style={{ 
                background: 'rgba(255,255,255,0.8)', 
                borderRadius: '8px' 
              }}>
                <h6 className="text-dark">🎯 Что теперь доступно:</h6>
                <ul className="list-unstyled mb-0 text-dark">
                  <li>🏴‍☠️ <strong>Пиратский переводчик</strong> в чате</li>
                  <li>⚡ <strong>Премиум статус</strong> в профиле</li>
                  <li>🎨 <strong>Эксклюзивные фичи</strong> в будущем</li>
                </ul>
              </div>

              <div className="d-grid gap-2">
                <Button 
                  variant="dark" 
                  size="lg"
                  onClick={() => navigate('/')}
                  style={{ fontWeight: 'bold' }}
                >
                  🚀 Перейти к чату
                </Button>
                
                <small className="text-muted">
                  Автоматический переход через 5 секунд...
                </small>
              </div>
            </Card.Body>
          </Card>
        </div>
      </div>
    </Container>
  );
}

export default PaymentSuccess;
