/**
 * 🏴‍☠️ СЕРВИС ПИРАТСКОЙ СТИЛИЗАЦИИ
 * 
 * Взаимодействует с backend API для стилизации текста
 */

import apiClient from './api.service';

class PirateService {
  /**
   * Превращает обычный текст в пиратский
   * @param {string} text - Исходный текст
   * @returns {Promise<Object>} - Результат стилизации
   */
  async piratifyText(text) {
    try {
      const response = await apiClient.post('/pirate/transform', {
        text: text,
        style: 'pirate'
      });
      
      return response.data;
    } catch (error) {
      console.error('❌ Ошибка стилизации:', error);
      
      // Fallback на локальную стилизацию если API недоступен
      return this.localPiratify(text);
    }
  }

  /**
   * Получает случайное пиратское восклицание
   * @returns {Promise<string>} - Пиратское восклицание
   */
  async getExclamation() {
    try {
      const response = await apiClient.get('/pirate/exclamation');
      return response.data.exclamation;
    } catch (error) {
      console.error('❌ Ошибка получения восклицания:', error);
      return this.getRandomExclamation();
    }
  }

  /**
   * Тестирует пиратский сервис
   * @returns {Promise<Object>} - Результаты тестов
   */
  async testService() {
    try {
      const response = await apiClient.get('/pirate/test');
      return response.data;
    } catch (error) {
      console.error('❌ Ошибка тестирования:', error);
      throw error;
    }
  }

  /**
   * Локальная стилизация (fallback)
   * @param {string} text - Исходный текст
   * @returns {Object} - Результат стилизации
   */
  localPiratify(text) {
    const pirateEndings = [' arr!', ' йо-хо-хо!', ', старый волк!', ', морской дьявол!'];
    
    const replacements = {
      'привет': 'йо-хо-хо',
      'как дела': 'как житуха',
      'спать': 'вешать чёрные метки',
      'есть': 'набивать трюм',
      'пить': 'промочить горло',
      'деньги': 'пиастры',
      'друг': 'старый пройдоха',
      'до свидания': 'попутного ветра'
    };

    let result = text.toLowerCase();
    
    // Применяем замены
    for (const [old_word, new_word] of Object.entries(replacements)) {
      if (result.includes(old_word)) {
        result = result.replace(old_word, new_word);
      }
    }

    // Добавляем пиратское окончание
    const randomEnding = pirateEndings[Math.floor(Math.random() * pirateEndings.length)];
    result += randomEnding;

    return {
      original_text: text,
      pirate_text: result.charAt(0).toUpperCase() + result.slice(1),
      style: 'pirate',
      success: true,
      fallback: true
    };
  }

  /**
   * Локальные восклицания (fallback)
   * @returns {string} - Случайное восклицание
   */
  getRandomExclamation() {
    const exclamations = [
      'Йо-хо-хо!',
      'Arr!',
      'Карамба!',
      'Тысяча чертей!',
      'Разрази меня гром!',
      'Кальмарьи кишки!',
      'Проклятье медузы!'
    ];
    
    return exclamations[Math.floor(Math.random() * exclamations.length)];
  }

  /**
   * Проверяет доступность пиратского API
   * @returns {Promise<boolean>} - Доступен ли API
   */
  async isApiAvailable() {
    try {
      await this.getExclamation();
      return true;
    } catch {
      return false;
    }
  }
}

export default new PirateService();
