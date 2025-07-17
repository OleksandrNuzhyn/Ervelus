import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  { path: '/login', name: 'login', component: () => import('@/views/LoginPage.vue'), meta: { guest: true } },
  { path: '/register', name: 'register', component: () => import('@/views/RegisterPage.vue'), meta: { guest: true } },
  { path: '/forgot-password', name: 'forgot-password', component: () => import('@/views/ForgotPasswordPage.vue') },
  { path: '/reset-password-confirm/:uid/:token', name: 'reset-password-confirm', component: () => import('@/views/ResetPasswordConfirmPage.vue') },
  { path: '/dashboard', name: 'dashboard', component: () => import('@/views/DashboardPage.vue'), meta: { requiresAuth: true } },
  {path: '/verify-email/:token', name: 'verify-email', component: () => import('@/views/ConfirmEmailPage.vue') },
  { path: '/', name: 'home-root', component: () => import('@/views/HomePage.vue') },
  { path: '/terms-of-service', name: 'terms-of-service', component: () => import('@/views/TermsOfServicePage.vue') },
  { path: '/privacy-policy', name: 'privacy-policy', component: () => import('@/views/PrivacyPolicyPage.vue') },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();

  if (!authStore.authChecked) {
    await authStore.checkAuth();
  }

  if (authStore.isAuthenticated && to.meta.guest) {
    return { path: from.fullPath };
  }  

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' };
  }
});

export default router;