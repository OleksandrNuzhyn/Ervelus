import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isMaintenanceMode: false
  }),
  actions: {
    setMaintenanceMode(status) {
      this.isMaintenanceMode = status;
    },
    async telegramAuth() {
      try {
        // DEBUG: Показуємо initData прямо на екрані, щоб перевірити в боті
        alert("TG Init Data: " + window.Telegram?.WebApp?.initData);

        console.log("TG Init Data:", window.Telegram?.WebApp?.initData);
        const { data } = await api.post('/api/telegram/auth/', {
          initData: window.Telegram?.WebApp?.initData
        });

        if (data.token) {
          localStorage.setItem('user-token', data.token);
          this.user = true;
        }
      }
      catch (error) {
        this.user = null;
      }
    }
  }
});