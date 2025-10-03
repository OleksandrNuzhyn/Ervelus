import './assets/base.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import GoogleSignInPlugin from 'vue3-google-signin'
import { initializePaddle } from '@paddle/paddle-js';

import App from './App.vue'
import router from './router'
import api from './services/api'

async function initializeApp() {
  await api.get('/api/auth/csrf-token/');

  await initializePaddle({
    token: 'test_d1b7d123c2e298499433b486045',
    environment: 'sandbox',
    checkout: {
      settings: {
        theme: 'dark',
        displayMode: 'overlay'
      }
    }
  });

  const app = createApp(App)
  const pinia = createPinia()
  
  app.use(pinia)
  app.use(router)
  app.use(GoogleSignInPlugin, {
    clientId: '533652113906-hnenie5h5ge7fou1ctvno0l0f748ginl.apps.googleusercontent.com'
  });
  
  app.mount('#app')
}

initializeApp();