/**
 * API SERVICE
 * 
 * Обёртка для axios с базовой конфигурацией
 */

import api from '../utils/axios';

// Экспортируем настроенный экземпляр axios как apiClient
const apiClient = api;

export default apiClient;
