import api from '../utils/axios';

const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await api.post('/auth/login/', formData.toString(), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

const register = async ({ username, email, password }) => {
  // Форматируем данные в соответствии со схемой UserCreate
  const userData = {
    username,
    email,
    password,
    is_active: true
  };
  console.log('Register data:', userData);
  const response = await api.post('/auth/register/', userData);
  return response.data;
};

const getCurrentUser = async () => {
  const response = await api.get('/users/me/');
  return response.data;
};

const authService = {
  login,
  register,
  getCurrentUser,
};

export default authService; 