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
  clientId: '281870812434-c175ecrljg0b8fr5sg30olverjkri2d0.apps.googleusercontent.com'
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