import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { show } from '@/services/terms';
import { toast } from './toast';

const api = axios.create({
  baseURL: 'https://ervelus-web-service-281870812434.us-central1.run.app',
  withCredentials: true
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('user-token');
    
    if (typeof token === 'string' && token) {
      config.headers['Authorization'] = `Token ${token}`;
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
    const originalRequest = error.config;
    const authStore = useAuthStore();

    if (error.response && error.response.status === 401) {
      const requestUrl = originalRequest.url || "";
      
      if (requestUrl.endsWith('/api/auth/user/')) {
        if (localStorage.getItem('user-token')) {
          toast.info("Your session has expired. Please sign in again");
          authStore.user = null;
          authStore.authChecked = true;
          localStorage.removeItem('user-token');
          const router = (await import('@/router')).default;
          await router.push({ name: 'login' });
        }
      }
      else if (authStore.isAuthenticated && !requestUrl.endsWith('/api/auth/logout/')) {
        toast.info("Your session has expired. Please sign in again");
        authStore.user = null;
        authStore.authChecked = true;
        localStorage.removeItem('user-token');
        const router = (await import('@/router')).default;
        await router.push({ name: 'login' });
      }
      return Promise.resolve();
    }

    if (error.response && error.response.status === 428) {
      const requiredAgreements = error.response.data?.required_agreements;
      if (requiredAgreements) {
        show(requiredAgreements);
      }
      return new Promise(() => {});
    }

    if (error.response && error.response.status === 429) {
      const message = error.response.data?.detail;
      if (message) {
        toast.info(message);
      }
      else {
        toast.info("You are making too many requests. Please try again in a moment");
      }
      return Promise.resolve();
    }

    if (error.response && error.response.status === 500) {
      toast.info("Oh! Something went wrong. Dwarves are already working on it");
      return Promise.reject(error);
    }

    if (error.response && error.response.status === 503 && error.response.data?.maintenance_mode === true) {
      authStore.setMaintenanceMode(true);
      return Promise.resolve();
    }

    return Promise.reject(error);
  }
);

export default api;