import api from '../utils/axios';

const convertToAscii = async (file, style = 'extended') => {
  const formData = new FormData();
  formData.append('file', file);
  
  console.log('File being sent:', file);
  console.log('File name:', file.name);
  console.log('File size:', file.size);
  console.log('File type:', file.type);
  console.log('Selected style:', style);
  
  // Выводим содержимое formData для отладки
  for (let pair of formData.entries()) {
    console.log(pair[0] + ': ' + pair[1]);
  }
  
  // Добавляем отладочный заголовок для отслеживания запроса
  const response = await api.post(`/ascii-art/convert/?style=${style}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'X-Debug': 'true'
    },
  });
  return response.data;
};

const getAvailableStyles = () => {
  return [
    { value: 'classic', label: 'Классический ASCII' },
    { value: 'unicode', label: 'Расширенный Unicode' },
    { value: 'blocks', label: 'Блочный стиль' },
    { value: 'extended', label: 'Максимальная детализация' }
  ];
};

const asciiService = {
  convertToAscii,
  getAvailableStyles
};

export default asciiService; 