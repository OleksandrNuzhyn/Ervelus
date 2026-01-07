import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomePage.vue'), meta: { guest: true, title: 'Ervelus - Transform Your Photos into AI Art' } },
  { path: '/login', name: 'login', component: () => import('@/views/LoginPage.vue'), meta: { guest: true, title: 'Login - Ervelus' } },
  { path: '/register', name: 'register', component: () => import('@/views/RegisterPage.vue'), meta: { guest: true, title: 'Register - Ervelus' } },
  { path: '/forgot-password', name: 'forgot-password', component: () => import('@/views/ForgotPasswordPage.vue'), meta: { title: 'Forgot Password - Ervelus' } },
  { path: '/reset-password-confirm/:uid/:token', name: 'reset-password-confirm', component: () => import('@/views/ResetPasswordConfirmPage.vue'), meta: { title: 'Reset Password - Ervelus' } },
  { path: '/verify-email/:token', name: 'verify-email', component: () => import('@/views/ConfirmEmailPage.vue'), meta: { title: 'Verify Email - Ervelus' } },
  { path: '/terms-of-service', name: 'terms-of-service', component: () => import('@/views/TermsOfServicePage.vue'), meta: { title: 'Terms of Service - Ervelus' } },
  { path: '/privacy-policy', name: 'privacy-policy', component: () => import('@/views/PrivacyPolicyPage.vue'), meta: { title: 'Privacy Policy - Ervelus' } },
  { path: '/refund-policy', name: 'refund-policy', component: () => import('@/views/RefundPolicyPage.vue'), meta: { title: 'Refund Policy - Ervelus' } },
  { path: '/cookie-policy', name: 'cookie-policy', component: () => import('@/views/CookiePolicyPage.vue'), meta: { title: 'Cookie Policy - Ervelus' } },
  { path: '/pricing', name: 'pricing', component: () => import('@/views/PricingPage.vue'), meta: { title: 'Pricing - Ervelus' } },
  { path: '/contact-us', name: 'contact-us', component: () => import('@/views/ContactUsPage.vue'), meta: { title: 'Contact Us - Ervelus' } },
  { path: '/dashboard', name: 'dashboard', component: () => import('@/views/GenerationPage.vue'), meta: { requiresAuth: true, title: 'Dashboard - Ervelus' } },
  { path: '/gallery', name: 'gallery', component: () => import('@/views/GalleryPage.vue'), meta: { requiresAuth: true, title: 'Gallery - Ervelus' } },
  { path: '/profile', name: 'profile', component: () => import('@/views/ProfilePage.vue'), meta: { requiresAuth: true, title: 'Profile - Ervelus' } },
  { path: '/about-us', name: 'about-us', component: () => import('@/views/AboutUsPage.vue'), meta: { title: 'About Us - Ervelus' } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from) => {
  document.title = to.meta.title || 'Ervelus';

  const authStore = useAuthStore();

  if (!authStore.authChecked) {
    await authStore.checkAuth();
  }

  if (authStore.isAuthenticated && to.meta.guest) {
    if (to.name === 'home' && from.name) {
      return;
    }

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