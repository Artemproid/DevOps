import React, { useState, useEffect } from 'react';
import { Button, Card, Alert, Spinner, Badge, Modal } from 'react-bootstrap';
import { useAuth } from '../../hooks/useAuth';
import api from '../../utils/axios';

function PremiumSubscription({ onSubscriptionChange }) {
  const { currentUser } = useAuth();
  const [subscriptionStatus, setSubscriptionStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchSubscriptionStatus();
  }, []);

  const fetchSubscriptionStatus = async () => {
    try {
      setLoading(true);
      const response = await api.get('/payments/subscription-status');
      setSubscriptionStatus(response.data);
      if (onSubscriptionChange) {
        onSubscriptionChange(response.data.is_premium);
      }
    } catch (error) {
      setError('Ошибка загрузки статуса подписки');
      console.error('Subscription status error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async () => {
    try {
      setProcessing(true);
      setError('');

      const checkoutData = {
        success_url: `${window.location.origin}/premium/success`,
        cancel_url: `${window.location.origin}/premium/cancel`
      };

      const response = await api.post('/payments/create-checkout-session', checkoutData);
      
      // Перенаправляем на Stripe Checkout
      window.location.href = response.data.checkout_url;
      
    } catch (error) {
      setError(error.response?.data?.detail || 'Ошибка создания платежной сессии');
      console.error('Checkout error:', error);
    } finally {
      setProcessing(false);
    }
  };

  const handleCancel = async () => {
    try {
      setProcessing(true);
      setError('');

      await api.post('/payments/cancel-subscription');
      
      // Обновляем статус
      await fetchSubscriptionStatus();
      setShowModal(false);
      
    } catch (error) {
      setError(error.response?.data?.detail || 'Ошибка отмены подписки');
      console.error('Cancel error:', error);
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <Card className="mb-3">
        <Card.Body className="text-center">
          <Spinner animation="border" size="sm" />
          <span className="ms-2">Загрузка статуса подписки...</span>
        </Card.Body>
      </Card>
    );
  }

  return (
    <>
      <Card className="mb-1" style={{ 
        background: subscriptionStatus?.is_premium ? 
          'linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)' : 
          'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)',
        minHeight: 'auto'
      }}>
        <Card.Body className="py-1 px-3">
          <div className="d-flex align-items-center justify-content-between">
            <div>
              <span className="fw-bold small">
                🏴‍☠️ Пиратский режим 
                {subscriptionStatus?.is_premium ? (
                  <Badge bg="success" className="ms-2">ON</Badge>
                ) : (
                  <Badge bg="secondary" className="ms-2">OFF</Badge>
                )}
              </span>
            </div>
            
            <div>
              {subscriptionStatus?.is_premium ? (
                <Button 
                  variant="outline-danger" 
                  size="sm"
                  onClick={() => setShowModal(true)}
                  disabled={processing}
                >
                  {processing ? (
                    <>
                      <Spinner animation="border" size="sm" className="me-2" />
                      Обработка...
                    </>
                  ) : (
                    'Отменить'
                  )}
                </Button>
              ) : (
                <Button 
                  variant="warning" 
                  onClick={handleSubscribe}
                  disabled={processing}
                  style={{ fontWeight: 'bold' }}
                >
                  {processing ? (
                    <>
                      <Spinner animation="border" size="sm" className="me-2" />
                      Обработка...
                    </>
                  ) : (
                    '⚡ Купить Premium'
                  )}
                </Button>
              )}
            </div>
          </div>



          {error && (
            <Alert variant="danger" className="mt-3 mb-0">
              {error}
            </Alert>
          )}
        </Card.Body>
      </Card>

      {/* Модал подтверждения отмены */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Отмена подписки</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Вы уверены, что хотите отменить премиум подписку?</p>
          <p className="text-muted">
            После отмены у вас больше не будет доступа к пиратскому режиму.
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Оставить подписку
          </Button>
          <Button 
            variant="danger" 
            onClick={handleCancel}
            disabled={processing}
          >
            {processing ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                Отменяю...
              </>
            ) : (
              'Да, отменить'
            )}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default PremiumSubscription;
