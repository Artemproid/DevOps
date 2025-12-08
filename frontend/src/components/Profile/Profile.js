import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Spinner, Alert } from 'react-bootstrap';
import { useAuth } from '../../hooks/useAuth';
import userService from '../../services/user.service';
import './Profile.css';

// Список доступных аватарок
const AVATAR_OPTIONS = [
  { id: 1, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix', name: 'Felix' },
  { id: 2, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Aneka', name: 'Aneka' },
  { id: 3, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Max', name: 'Max' },
  { id: 4, url: 'https://api.dicebear.com/7.x/bottts/svg?seed=Robot1', name: 'Robot' },
  { id: 5, url: 'https://api.dicebear.com/7.x/bottts/svg?seed=Robot2', name: 'Droid' },
  { id: 6, url: 'https://api.dicebear.com/7.x/pixel-art/svg?seed=Pixel1', name: 'Pixel' },
  { id: 7, url: 'https://api.dicebear.com/7.x/pixel-art/svg?seed=Pixel2', name: 'Retro' },
  { id: 8, url: 'https://api.dicebear.com/7.x/identicon/svg?seed=Geo1', name: 'Geo' },
  { id: 9, url: 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=Happy', name: 'Happy' },
  { id: 10, url: 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=Cool', name: 'Cool' },
  { id: 11, url: 'https://api.dicebear.com/7.x/lorelei/svg?seed=Girl1', name: 'Luna' },
  { id: 12, url: 'https://api.dicebear.com/7.x/lorelei/svg?seed=Boy1', name: 'Max' },
];

function Profile({ show, onHide }) {
  const { currentUser, refreshUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [selectedAvatar, setSelectedAvatar] = useState('');
  const [bio, setBio] = useState('');

  useEffect(() => {
    if (currentUser) {
      setSelectedAvatar(currentUser.avatar_url || '');
      setBio(currentUser.bio || '');
    }
  }, [currentUser]);

  const handleSave = async () => {
    try {
      setLoading(true);
      setError('');
      setSuccess('');

      await userService.updateProfile({
        avatar_url: selectedAvatar,
        bio: bio
      });

      setSuccess('Профиль успешно обновлён!');
      
      // Обновляем данные пользователя
      if (refreshUser) {
        await refreshUser();
      }

      setTimeout(() => {
        onHide();
      }, 1500);

    } catch (err) {
      console.error('Error updating profile:', err);
      setError('Ошибка при сохранении профиля');
    } finally {
      setLoading(false);
    }
  };

  const getDisplayAvatar = () => {
    if (selectedAvatar) return selectedAvatar;
    if (currentUser?.username) {
      return `https://api.dicebear.com/7.x/initials/svg?seed=${currentUser.username}`;
    }
    return 'https://api.dicebear.com/7.x/identicon/svg?seed=default';
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title>👤 Мой профиль</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        <div className="profile-content">
          {/* Текущий аватар */}
          <div className="current-avatar-section">
            <h6>Текущий аватар</h6>
            <img 
              src={getDisplayAvatar()} 
              alt="Current Avatar" 
              className="current-avatar"
            />
            <div className="mt-2">
              <strong>{currentUser?.username}</strong>
              <br />
              <small className="text-muted">{currentUser?.email}</small>
            </div>
          </div>

          {/* Выбор аватара */}
          <div className="avatar-selection-section">
            <h6>Выберите аватар</h6>
            <div className="avatar-grid">
              {AVATAR_OPTIONS.map((avatar) => (
                <div 
                  key={avatar.id}
                  className={`avatar-option ${selectedAvatar === avatar.url ? 'selected' : ''}`}
                  onClick={() => setSelectedAvatar(avatar.url)}
                >
                  <img src={avatar.url} alt={avatar.name} />
                  <small>{avatar.name}</small>
                </div>
              ))}
            </div>
          </div>

          {/* Кастомный URL */}
          <Form.Group className="mt-3">
            <Form.Label>Или введите URL своего аватара</Form.Label>
            <Form.Control
              type="text"
              placeholder="https://example.com/avatar.png"
              value={selectedAvatar}
              onChange={(e) => setSelectedAvatar(e.target.value)}
            />
          </Form.Group>

          {/* Био */}
          <Form.Group className="mt-3">
            <Form.Label>О себе</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              placeholder="Расскажите о себе..."
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              maxLength={500}
            />
            <Form.Text className="text-muted">
              {bio.length}/500 символов
            </Form.Text>
          </Form.Group>
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Отмена
        </Button>
        <Button variant="primary" onClick={handleSave} disabled={loading}>
          {loading ? (
            <>
              <Spinner size="sm" className="me-2" />
              Сохранение...
            </>
          ) : (
            '💾 Сохранить'
          )}
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default Profile;
