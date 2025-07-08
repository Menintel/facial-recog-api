import axios from 'axios';
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  // Add a request interceptor to include the JWT token
  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('accessToken'); // Assuming token is stored in localStorage
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  
  export default api;