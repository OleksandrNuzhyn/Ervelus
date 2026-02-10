import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { show } from '@/services/terms';

const api = axios.create({
  baseURL: 'https://ervelus-web-service-324377414272.us-central1.run.app',
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

let isReloading = false;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore();

    if (error.response && error.response.status === 401) {
      if (authStore.user) {
        if (!isReloading) {
          isReloading = true;
          authStore.user = null;
          localStorage.removeItem('user-token');
          window.location.reload();
        }
        return new Promise(() => {});
      }
      return Promise.reject(error);
    }

    if (error.response && error.response.status === 428) {
      const requiredAgreements = error.response.data?.required_agreements;
      if (requiredAgreements) {
        show(requiredAgreements);
      }
      return new Promise(() => {});
    }

    if (error.response && error.response.status === 503 && error.response.data?.maintenance_mode === true) {
      authStore.setMaintenanceMode(true);
      return Promise.resolve();
    }

    return Promise.reject(error);
  }
);

export default api;