import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import UserSearch from '../UserSearch/UserSearch';

function Header() {
  const { isAuthenticated, currentUser, logout } = useAuth();

  const handleUserSelect = (user) => {
    // Переходим к приватному чату с пользователем
    window.location.href = `/chat/${user.id}`;
  };

  return (
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
                <Navbar.Text className="me-3">
                  Welcome, {currentUser?.username}
                </Navbar.Text>
                <Button variant="outline-light" onClick={logout}>Logout</Button>
              </>
            ) : (
              <>
                <Nav.Link as={Link} to="/login">Login</Nav.Link>
                <Nav.Link as={Link} to="/register">Register</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header; 