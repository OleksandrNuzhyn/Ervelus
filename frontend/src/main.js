import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

async function initializeApp() {
  const authStore = useAuthStore();
  
  // Чекаємо на першу перевірку статусу
  await authStore.checkAuth();
  
  app.use(router);

  if (authStore.isAuthenticated && router.currentRoute.value.path === '/') {
    // Якщо користувач залогінений і знаходиться на головній сторінці,
    // відправляємо його на дашборд.
    router.push('/dashboard');
  }
  
  app.mount('#app');
}

initializeApp();