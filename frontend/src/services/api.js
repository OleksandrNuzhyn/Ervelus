import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { toast } from './toast';

const api = axios.create({
  baseURL: 'https://ervelus-web-service-281870812434.us-central1.run.app',
  withCredentials: true
});

api.interceptors.request.use(
  async (config) => {
    const authStore = useAuthStore();
    
    const unsafeMethods = ['POST', 'PUT', 'PATCH', 'DELETE'];
    if (unsafeMethods.includes(config.method.toUpperCase())) {
      try {
        const csrfToken = await authStore.fetchCsrfToken();
        if (csrfToken) {
          config.headers['X-CSRFToken'] = csrfToken;
        }
      }
      catch (error) {
        return Promise.reject(error);
      }
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
    const authStore = useAuthStore();

    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      const requestUrl = error.request.responseURL || "";

      if (!requestUrl.endsWith('/api/auth/user/')) {
        toast.info("Your session has expired. Please sign in again");
        authStore.logout();
        const router = (await import('@/router')).default;
        await router.push({ name: 'login' });
        return Promise.resolve();
      }
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
    }

    if (error.response && error.response.status === 503 && error.response.data?.maintenance_mode === true) {
      authStore.setMaintenanceMode(true);
      return Promise.resolve();
    }

    return Promise.reject(error);
  }
);

export default api;