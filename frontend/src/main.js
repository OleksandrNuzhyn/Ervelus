import './assets/base.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import GoogleSignInPlugin from 'vue3-google-signin';

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(GoogleSignInPlugin, {
  clientId: '843713679678-0uev2hp893rnt24bm6rujisimkfocqbv.apps.googleusercontent.com'
});

app.mount('#app')
