import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { toast } from './toast';

export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const api = axios.create({
  withCredentials: true,
});

api.interceptors.request.use(
  (config) => {
    const csrfToken = getCookie('csrftoken'); 

    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      authStore.$reset();
      const router = (await import('@/router')).default;
      await router.push({ name: 'login' });
      return Promise.resolve();
    }

    if (error.response && error.response.status === 500) {
      toast.info("Oh! Something went wrong. Dwarves are already working on it. Please try again later.");
    }

    return Promise.reject(error);
  }
);

export default api;