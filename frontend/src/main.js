import './assets/base.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'
import { useAuthStore } from '@/stores/auth'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(vue3GoogleLogin, {
    clientId: '843713679678-0uev2hp893rnt24bm6rujisimkfocqbv.apps.googleusercontent.com'
  })

const pinia = createPinia()
app.use(pinia)
app.use(router)

useAuthStore().checkAuth()

app.mount('#app')
