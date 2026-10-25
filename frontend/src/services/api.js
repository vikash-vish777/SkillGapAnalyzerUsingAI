import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Ensure multipart boundary is generated automatically by browser for FormData
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle common errors gracefully
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      // Server returned error status code (4xx, 5xx)
      const data = error.response.data;
      const message = data?.message || 'An unexpected error occurred.';
      return Promise.reject(new Error(message));
    } else if (error.request) {
      // Request was made but no response received (network issue / server down)
      return Promise.reject(new Error('Cannot connect to backend server. Please verify it is running.'));
    }
    return Promise.reject(error);
  }
);

export default api;

