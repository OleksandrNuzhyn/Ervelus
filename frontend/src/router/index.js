import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomePage.vue') },
  { path: '/login', name: 'login', component: () => import('@/views/LoginPage.vue'), meta: { guest: true } },
  { path: '/register', name: 'register', component: () => import('@/views/RegisterPage.vue'), meta: { guest: true } },
  { path: '/forgot-password', name: 'forgot-password', component: () => import('@/views/ForgotPasswordPage.vue') },
  { path: '/reset-password-confirm/:uid/:token', name: 'reset-password-confirm', component: () => import('@/views/ResetPasswordConfirmPage.vue') },
  { path: '/verify-email/:token', name: 'verify-email', component: () => import('@/views/ConfirmEmailPage.vue') },
  { path: '/terms-of-service', name: 'terms-of-service', component: () => import('@/views/TermsOfServicePage.vue') },
  { path: '/privacy-policy', name: 'privacy-policy', component: () => import('@/views/PrivacyPolicyPage.vue') },
  { path: '/dmca-policy', name: 'dmca-policy', component: () => import('@/views/DMCAPolicyPage.vue') },
  { path: '/pricing', name: 'pricing', component: () => import('@/views/PricingPage.vue') },
  { path: '/contact-us', name: 'contact-us', component: () => import('@/views/ContactUsPage.vue') },
  { path: '/dashboard', name: 'dashboard', component: () => import('@/views/GenerationPage.vue'), meta: { requiresAuth: true } },
  { path: '/gallery', name: 'gallery', component: () => import('@/views/GalleryPage.vue'), meta: { requiresAuth: true } },
  { path: '/profile', name: 'profile', component: () => import('@/views/ProfilePage.vue'), meta: { requiresAuth: true } }
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
    return { name: 'dashboard' };
  }  

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' };
  }
});

router.onError((error, to) => {
  if (error.message.includes('Failed to fetch dynamically imported module') && window.navigator.onLine) {
    window.location = to.fullPath;
  }
});

export default router;