import React, { useEffect } from 'react';
import { Container, Card, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function PaymentCancel() {
  const navigate = useNavigate();

  useEffect(() => {
    // Автоматический редирект через 5 секунд
    const timer = setTimeout(() => {
      navigate('/');
    }, 5000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <Container className="mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <Card className="text-center" style={{ 
            background: 'linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%)',
            border: '3px solid #dc3545'
          }}>
            <Card.Body className="p-5">
              <div className="mb-4">
                <div style={{ fontSize: '4rem' }}>😔</div>
                <h2 className="text-dark">Оплата отменена</h2>
              </div>
              
              <Alert variant="warning" className="mb-4">
                <h5>💳 Платёж был отменён</h5>
                <p className="mb-0">
                  Ничего страшного! Вы можете оформить подписку в любое время.
                </p>
              </Alert>

              <div className="mb-4 p-3" style={{ 
                background: 'rgba(255,255,255,0.8)', 
                borderRadius: '8px' 
              }}>
                <h6 className="text-dark">🏴‍☠️ Пиратский режим ждёт вас!</h6>
                <p className="text-dark mb-0">
                  Оформите премиум подписку, чтобы разблокировать эксклюзивные возможности:
                </p>
                <ul className="list-unstyled mt-2 mb-0 text-dark">
                  <li>🗣️ Пиратская стилизация сообщений</li>
                  <li>⚡ Приоритетная поддержка</li>
                  <li>🎨 Новые фичи первыми</li>
                </ul>
              </div>

              <div className="d-grid gap-2">
                <Button 
                  variant="primary" 
                  size="lg"
                  onClick={() => navigate('/')}
                  style={{ fontWeight: 'bold' }}
                >
                  🔙 Вернуться к чату
                </Button>
                
                <Button 
                  variant="outline-warning"
                  onClick={() => navigate('/')}
                >
                  💳 Попробовать оплатить снова
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

export default PaymentCancel;
