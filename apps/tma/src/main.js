import './assets/base.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n.js'
import telegramAnalytics from '@telegram-apps/analytics';

telegramAnalytics.init({
    token: 'eyJhcHBfbmFtZSI6IkVydmVsdXMiLCJhcHBfdXJsIjoiaHR0cHM6Ly90Lm1lL2VydmVsdXNfYm90IiwiYXBwX2RvbWFpbiI6Imh0dHBzOi8vdG1hLmVydmVsdXMuY29tLyJ9!oZRUO9+KQ0ZRAkTzv+HwY6YDx52tngcHzCysXu7p6bY=',
    appName: 'Ervelus'
});

import { createApp } from 'vue'
import { createPinia } from 'pinia'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)

app.mount('#app')