import api from '../utils/axios';

const searchUsers = async (query) => {
  const response = await api.get(`/users/search/?q=${encodeURIComponent(query)}`);
  return response.data;
};

const getUser = async (userId) => {
  const response = await api.get(`/users/${userId}/`);
  return response.data;
};

const getAllUsers = async (skip = 0, limit = 100) => {
  const response = await api.get(`/users/?skip=${skip}&limit=${limit}`);
  return response.data;
};

const updateProfile = async (profileData) => {
  const response = await api.put('/users/me/profile/', profileData);
  return response.data;
};

const userService = {
  searchUsers,
  getUser,
  getAllUsers,
  updateProfile,
};

export default userService;
