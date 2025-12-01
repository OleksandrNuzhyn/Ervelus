import './assets/base.css'
import App from './App.vue'
import router from './router'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { initializePaddle } from '@paddle/paddle-js';
import GoogleSignInPlugin from 'vue3-google-signin'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(GoogleSignInPlugin, {
  clientId: '324377414272-g7rqnvo9n7lb5ugsb9q1a15u0lul0255.apps.googleusercontent.com'
});

app.mount('#app')

initializePaddle({
  token: 'test_d1b7d123c2e298499433b486045',
  environment: 'sandbox',
  checkout: {
    settings: {
      theme: 'dark',
      displayMode: 'overlay'
    }
  }
});