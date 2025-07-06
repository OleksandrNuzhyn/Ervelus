import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  { path: '/login', name: 'login', component: () => import('@/views/LoginPage.vue') },
  { path: '/register', name: 'register', component: () => import('@/views/RegisterPage.vue') },
  //{ path: '/dashboard', name: 'dashboard', component: () => import('@/views/DashboardPage.vue'), meta: { requiresAuth: true } },
  //{ path: '/', name: 'home', component: () => import('@/views/HomePage.vue') }
  { path: '/forgot-password', name: 'forgot-password', component: () => import('@/components/AuthComponents/ForgotPasswordForm.vue') },
  { path: '/reset-password-confirm/:uid/:token', name: 'reset-password-confirm', component: () => import('@/components/AuthComponents/ResetPasswordConfirm.vue') },
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