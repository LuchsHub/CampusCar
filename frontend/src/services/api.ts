import axios from 'axios';
import { useAuthStore } from '@/stores/AuthStore';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  withCredentials: true, // if you need to send cookies (e.g., for auth)
});

// Request interceptor (e.g., to add auth tokens)
api.interceptors.request.use(
  (config) => {
    // Add auth token from AuthStore if available
    const authStore = useAuthStore();
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor (e.g., for global error handling)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Optionally handle errors globally
    // Example: if (error.response?.status === 401) { ... }
    return Promise.reject(error);
  }
);

export default api; 