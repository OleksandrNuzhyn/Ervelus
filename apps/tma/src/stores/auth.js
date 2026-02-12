import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    is_subscribed: false,
    isMaintenanceMode: false
  }),
  actions: {
    setMaintenanceMode(status) {
      this.isMaintenanceMode = status;
    },
    async telegramAuth() {
      try {
        const { data } = await api.post('/api/telegram/auth/', {
          initData: window.Telegram?.WebApp?.initData
        });

        if (data.token) {
          localStorage.setItem('user-token', data.token);
          this.user = true;
          this.is_subscribed = data.is_subscribed;
        }
      }
      catch (error) {
        this.user = null;
        this.is_subscribed = false;
      }
    }
  }
});