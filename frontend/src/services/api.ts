import axios from 'axios';

const api = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Cache-Control': 'no-cache'
  },
  withCredentials: false
});

// Initialize auth header if token exists
const token = localStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      // Ensure headers object exists
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
      console.debug('Request headers:', config.headers);
      console.debug('Request URL:', config.url);
    } else {
      console.debug('No token found in localStorage');
    }
    return config;
  },
  error => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  response => {
    console.debug('Response received:', {
      url: response.config.url,
      status: response.status,
      data: response.data
    });
    return response;
  },
  error => {
    console.error('Response interceptor error:', {
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    
    if (error.response?.status === 401) {
      console.debug('Unauthorized request detected');
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
      // Don't redirect automatically, let components handle navigation
    }
    return Promise.reject(error);
  }
);

export default api;