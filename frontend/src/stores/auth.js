import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    authChecked: false
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
  },
  actions: {
    logout() {
      this.user = null;
      this.authChecked = true;
    },
    async checkAuth() {
      try {
        const { data } = await api.get('/api/auth/user/');
        this.user = data;
      } 
      catch (error) {
        this.user = null;
      }
      finally {
        this.authChecked = true;
      }
    }
  }
});