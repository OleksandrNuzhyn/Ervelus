import './assets/base.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n.js'
import telegramAnalytics from '@telegram-apps/analytics';

telegramAnalytics.init({
    token: 'eyJhcHBfbmFtZSI6ImVydmVsdXMiLCJhcHBfdXJsIjoiaHR0cHM6Ly90Lm1lL2VydmVsdXNfYm90IiwiYXBwX2RvbWFpbiI6Imh0dHBzOi8vdG1hLmVydmVsdXMuY29tLyJ9!UUrLaNozpnJFR+KiYmjKll8ZJDJCr6xoBYP43+gafaM=',
    appName: 'ervelus'
});

import { createApp } from 'vue'
import { createPinia } from 'pinia'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)

app.mount('#app')