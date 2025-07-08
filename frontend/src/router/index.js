import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  { path: '/login', name: 'login', component: () => import('@/views/LoginPage.vue') },
  { path: '/register', name: 'register', component: () => import('@/views/RegisterPage.vue') },
  { path: '/forgot-password', name: 'forgot-password', component: () => import('@/views/ForgotPasswordPage.vue') },
  { path: '/reset-password-confirm/:uid/:token', name: 'reset-password-confirm', component: () => import('@/views/ResetPasswordConfirmPage.vue') },
  { path: '/dashboard', name: 'dashboard', component: () => import('@/views/DashboardPage.vue'), meta: { requiresAuth: true } },
  { path: '/', redirect: '/dashboard' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const authStore = useAuthStore();

  if (!authStore.user) {
    await authStore.checkAuth();
  }
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } };
  }
});

export default router;