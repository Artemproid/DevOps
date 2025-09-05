class WebSocketService {
  constructor() {
    this.ws = null;
    this.token = null;
    this.url = 'ws://localhost:8080/api/ws/ws';
    this.reconnectInterval = 5000;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.listeners = {};
  }

  connect(token) {
    // Если уже подключены с тем же токеном, не переподключаемся
    if (this.ws && this.ws.readyState === WebSocket.OPEN && this.token === token) {
      console.log('WebSocket already connected');
      return;
    }

    // Если уже идёт подключение, не создаём новое
    if (this.ws && this.ws.readyState === WebSocket.CONNECTING) {
      console.log('WebSocket is already connecting, skipping...');
      return;
    }

    this.token = token;
    
    if (this.ws) {
      console.log('Closing existing WebSocket connection');
      this.ws.close();
      this.ws = null;
    }

    try {
      console.log('Connecting WebSocket with token:', token ? 'present' : 'missing');
      this.ws = new WebSocket(`${this.url}?token=${encodeURIComponent(token)}`);
      
      this.ws.onopen = (event) => {
        console.log('✅ WebSocket connected successfully');
        this.reconnectAttempts = 0;
        this.emit('connected', event);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 WebSocket message received:', data);
          this.handleMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onclose = (event) => {
        console.log('❌ WebSocket disconnected:', event.code, event.reason);
        this.emit('disconnected', event);
        
        // Переподключаемся кроме случаев намеренного отключения или ошибок аутентификации
        if (event.code !== 1000 && event.code !== 1001 && event.code !== 4001) {
          this.attemptReconnect();
        } else if (event.code === 4001) {
          console.error('Authentication failed - token invalid');
          this.emit('auth_error', event);
        }
      };

      this.ws.onerror = (error) => {
        console.error('💥 WebSocket error:', error);
        this.emit('error', error);
      };

    } catch (error) {
      console.error('Error creating WebSocket connection:', error);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts && this.token) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect(this.token);
      }, this.reconnectInterval);
    }
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }

  handleMessage(data) {
    const { type } = data;
    this.emit(type, data);
  }

  // Event listener methods
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  off(event, callback) {
    if (!this.listeners[event]) return;
    
    this.listeners[event] = this.listeners[event].filter(
      listener => listener !== callback
    );
  }

  emit(event, data) {
    if (!this.listeners[event]) return;
    
    this.listeners[event].forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Error in ${event} listener:`, error);
      }
    });
  }

  // Chat-specific methods
  joinChat(chatId) {
    this.send({
      type: 'join_chat',
      chat_id: chatId
    });
  }

  leaveChat(chatId) {
    this.send({
      type: 'leave_chat',
      chat_id: chatId
    });
  }

  startTyping(chatId) {
    this.send({
      type: 'typing_start',
      chat_id: chatId
    });
  }

  stopTyping(chatId) {
    this.send({
      type: 'typing_stop',
      chat_id: chatId
    });
  }

  sendMessage(chatId, content) {
    this.send({
      type: 'send_message',
      chat_id: chatId,
      content: content
    });
  }

  getOnlineUsers() {
    this.send({
      type: 'get_online_users'
    });
  }

  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}

// Singleton instance
const websocketService = new WebSocketService();

export default websocketService;
