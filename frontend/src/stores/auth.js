import { defineStore } from 'pinia';
import router from '@/router';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    authStatus: 'pending',
  }),
  getters: {
    isAuthenticated: (state) => state.authStatus === 'loggedIn',
    isAuthReady: (state) => state.authStatus !== 'pending',
  },
  actions: {
    async checkAuth() {
      this.authStatus = 'pending';
      try {
        const response = await api.get('/api/auth/user/');
        this.user = response.data;
        this.authStatus = 'loggedIn';
      } catch (error) {
        this.user = null;
        this.authStatus = 'loggedOut';
      }
    },

    async register(credentials) {
      return api.post('/api/auth/registration/', credentials);
    },

    async login(credentials) {
      await api.post('/api/auth/login/', credentials);
      await this.checkAuth();
      const redirectPath = router.currentRoute.value.query.redirect || '/dashboard';
      router.push(redirectPath);
    },

    async logout() {
      await api.post('/api/auth/logout/');
      this.user = null;
      this.authStatus = 'loggedOut';
      router.push('/login');
    },
    
    async verifyEmail(key) {
      return api.post('/api/auth/registration/verify-email/', { key });
    },

    async requestPasswordReset(email) {
      return api.post('/api/auth/password/reset/', { email });
    },

    async confirmPasswordReset(payload) {
      return api.post('/api/auth/password/reset/confirm/', payload);
    },

    async handleGoogleLogin(accessToken) {
      await api.post('/api/auth/google/', { access_token: accessToken });
      await this.checkAuth();
      const redirectPath = router.currentRoute.value.query.redirect || '/dashboard';
      router.push(redirectPath);
    },
  },
});