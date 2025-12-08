import React, { useState } from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import UserSearch from '../UserSearch/UserSearch';
import Profile from '../Profile/Profile';

function Header() {
  const { isAuthenticated, currentUser, logout } = useAuth();
  const [showProfile, setShowProfile] = useState(false);

  const handleUserSelect = (user) => {
    // Переходим к приватному чату с пользователем
    window.location.href = `/chat/${user.id}`;
  };

  const getAvatarUrl = () => {
    if (currentUser?.avatar_url) return currentUser.avatar_url;
    return `https://api.dicebear.com/7.x/initials/svg?seed=${currentUser?.username || 'User'}`;
  };

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand as={Link} to="/">Social Network</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            {isAuthenticated && (
              <Nav className="me-auto">
                <UserSearch onUserSelect={handleUserSelect} />
              </Nav>
            )}
            <Nav className="ms-auto">
              {isAuthenticated ? (
                <>
                  <div 
                    className="d-flex align-items-center me-3" 
                    style={{ cursor: 'pointer' }}
                    onClick={() => setShowProfile(true)}
                  >
                    <img 
                      src={getAvatarUrl()} 
                      alt="Avatar" 
                      style={{ 
                        width: 32, 
                        height: 32, 
                        borderRadius: '50%',
                        marginRight: 8,
                        border: '2px solid #fff'
                      }}
                    />
                    <Navbar.Text>
                      {currentUser?.username}
                    </Navbar.Text>
                  </div>
                  <Button variant="outline-light" size="sm" onClick={logout}>Выход</Button>
                </>
              ) : (
                <>
                  <Nav.Link as={Link} to="/login">Вход</Nav.Link>
                  <Nav.Link as={Link} to="/register">Регистрация</Nav.Link>
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Модальное окно профиля */}
      <Profile show={showProfile} onHide={() => setShowProfile(false)} />
    </>
  );
}

export default Header; 