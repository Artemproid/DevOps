import axios from 'axios';

// В браузере используем относительные пути (они будут проксироваться через webpack dev server)
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log('Request:', {
      url: config.url,
      method: config.method,
      baseURL: config.baseURL,
      headers: config.headers
    });
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('Response:', {
      status: response.status,
      data: response.data
    });
    return response;
  },
  (error) => {
    console.error('Response Error:', error.response ? {
      status: error.response.status,
      data: error.response.data
    } : error.message);

    if (error.response) {
      // Handle 401 (Unauthorized)
      if (error.response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
      // Handle 307 (Temporary Redirect)
      else if (error.response.status === 307) {
        const newUrl = error.response.headers.location;
        // Если URL начинается с /, добавляем слэш в конце
        if (newUrl.startsWith('/') && !newUrl.endsWith('/')) {
          return api.request({
            ...error.config,
            url: `${newUrl}/`
          });
        }
        return api.request({
          ...error.config,
          url: newUrl
        });
      }
    }

    return Promise.reject(error);
  }
);

export default api; 