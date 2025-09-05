import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import Header from './components/Layout/Header';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import ChatLayout from './components/Chat/ChatLayout';
import PaymentSuccess from './components/Payment/PaymentSuccess';
import PaymentCancel from './components/Payment/PaymentCancel';
import { useAuth } from './hooks/useAuth';
import './App.css';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="App">
      <Header />
      <div className="app-content">
        <Routes>
        <Route path="/chat" element={isAuthenticated ? <ChatLayout /> : <Navigate to="/login" />} />
        <Route path="/chat/:userId" element={isAuthenticated ? <ChatLayout /> : <Navigate to="/login" />} />
        <Route path="/premium/success" element={isAuthenticated ? <PaymentSuccess /> : <Navigate to="/login" />} />
        <Route path="/premium/cancel" element={isAuthenticated ? <PaymentCancel /> : <Navigate to="/login" />} />
        <Route path="/login" element={!isAuthenticated ? <Container className="mt-4"><Login /></Container> : <Navigate to="/chat" />} />
        <Route path="/register" element={!isAuthenticated ? <Container className="mt-4"><Register /></Container> : <Navigate to="/chat" />} />
        <Route path="/" element={<Navigate to="/chat" />} />
        <Route path="*" element={<Navigate to="/chat" />} />
        </Routes>
      </div>
    </div>
  );
}

export default App; 