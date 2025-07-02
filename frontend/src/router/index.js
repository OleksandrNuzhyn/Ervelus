import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  // Автентифікація
  { path: '/login', name: 'login', component: () => import('@/views/LoginPage.vue') },
  { path: '/register', name: 'register', component: () => import('@/views/RegisterPage.vue') },
  { path: '/registration/check-email', name: 'check-email', component: () => import('@/views/CheckEmailPage.vue') },
  { path: '/verify-email/:key', name: 'verify-email', component: () => import('@/views/VerifyEmailPage.vue'), props: true },
  
  // Відновлення пароля
  { path: '/password-reset', name: 'password-reset', component: () => import('@/views/RequestPasswordResetPage.vue') },
  { path: '/password-reset/confirm/:uid/:token', name: 'password-reset-confirm', component: () => import('@/views/ConfirmPasswordResetPage.vue'), props: true },

  // Захищені сторінки
  // { path: '/dashboard', name: 'dashboard', component: () => import('@/views/DashboardPage.vue'), meta: { requiresAuth: true } },

  // Головна сторінка
  { path: '/', name: 'home', component: () => import('@/views/HomePage.vue') }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } };
  }
});

export default router;