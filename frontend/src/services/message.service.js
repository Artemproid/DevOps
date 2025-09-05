import api from '../utils/axios';

const getMessages = async (page = 0, limit = 100) => {
  const response = await api.get(`/messages/?skip=${page * limit}&limit=${limit}`);
  return response.data;
};

const getChatMessages = async (chatId, page = 0, limit = 100) => {
  const response = await api.get(`/messages/chat/${chatId}/?skip=${page * limit}&limit=${limit}`);
  return response.data;
};

const getPrivateMessages = async (userId, page = 0, limit = 100) => {
  const response = await api.get(`/messages/private/${userId}/?skip=${page * limit}&limit=${limit}`);
  return response.data;
};

const sendMessage = async (content, chatId, messageType = 'regular') => {
  const response = await api.post('/messages/', {
    content: content,
    chat_id: chatId,
    message_type: messageType
  });
  return response.data;
};

const messageService = {
  getMessages,
  getChatMessages,
  getPrivateMessages,
  sendMessage,
};

export default messageService; 