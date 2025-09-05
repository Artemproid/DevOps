import api from '../utils/axios';

// Получить список чатов пользователя
const getUserChats = async () => {
  const response = await api.get('/chats/');
  return response.data;
};

// Получить детальную информацию о чатах пользователя
const getUserChatsDetailed = async () => {
  const response = await api.get('/chats/detailed/');
  return response.data;
};

// Получить общий чат
const getPublicChat = async () => {
  const response = await api.get('/chats/public/');
  return response.data;
};

// Получить или создать приватный чат
const getOrCreatePrivateChat = async (userId) => {
  const response = await api.get(`/chats/private/${userId}/`);
  return response.data;
};

// Получить информацию о чате
const getChatInfo = async (chatId) => {
  const response = await api.get(`/chats/${chatId}/`);
  return response.data;
};

const chatService = {
  getUserChats,
  getUserChatsDetailed,
  getPublicChat,
  getOrCreatePrivateChat,
  getChatInfo,
};

export default chatService;