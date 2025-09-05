import React, { createContext, useState, useEffect } from 'react';
import authService from '../services/auth.service';
import websocketService from '../services/websocket.service';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      // Check if token exists and try to get user info
      if (token) {
        try {
          const user = await authService.getCurrentUser();
          setCurrentUser(user);
        } catch (error) {
          console.error('Error initializing auth:', error);
          // Only clear auth if it's an authentication error
          if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            setToken(null);
            setCurrentUser(null);
          }
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await authService.login(username, password);
      const { access_token } = response;
      localStorage.setItem('token', access_token);
      setToken(access_token);
      const user = await authService.getCurrentUser();
      setCurrentUser(user);
      return user;
    } catch (error) {
      console.error('Login error:', error);
      localStorage.removeItem('token');
      setToken(null);
      setCurrentUser(null);
      throw error;
    }
  };

  const register = async (userData) => {
    const newUser = await authService.register(userData);
    return newUser;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setCurrentUser(null);
    
    // Отключаем WebSocket при выходе
    websocketService.disconnect();
  };

  const value = {
    currentUser,
    token,
    isAuthenticated: !!token,
    loading,
    login,
    register,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}; 