import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    authChecked: false,
    isMaintenanceMode: false,
    csrfToken: null,
    csrfPromise: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
  },
  actions: {
    setMaintenanceMode(status) {
      this.isMaintenanceMode = status;
    },
    logout() {
      this.user = null;
      this.authChecked = true;
    },
    async fetchCsrfToken() {
      if (this.csrfToken) {
        return this.csrfToken;
      }
      
      if (!this.csrfPromise) {
        this.csrfPromise = api.get('/api/auth/csrf-token/').then(response => {
          this.csrfToken = response.data.csrf_token;
          this.csrfPromise = null;
          return this.csrfToken;
        }).catch(error => {
          this.csrfPromise = null;
          throw error;
        });
      }

      return this.csrfPromise;
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