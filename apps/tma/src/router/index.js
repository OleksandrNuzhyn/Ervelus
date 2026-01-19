import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  { path: '/', name: 'dashboard', component: () => import('@/views/GenerationPage.vue'), meta: { title: 'Dashboard' } },
  { path: '/gallery', name: 'gallery', component: () => import('@/views/GalleryPage.vue'), meta: { title: 'Gallery' } },
  { path: '/profile', name: 'profile', component: () => import('@/views/ProfilePage.vue'), meta: { title: 'Profile' } },
  { path: '/terms-of-service', name: 'terms-of-service', component: () => import('@/views/TermsOfServicePage.vue'), meta: { title: 'Terms of Service' } },
  { path: '/privacy-policy', name: 'privacy-policy', component: () => import('@/views/PrivacyPolicyPage.vue'), meta: { title: 'Privacy Policy' } },
  { path: '/refund-policy', name: 'refund-policy', component: () => import('@/views/RefundPolicyPage.vue'), meta: { title: 'Refund Policy' } },
  { path: '/cookie-policy', name: 'cookie-policy', component: () => import('@/views/CookiePolicyPage.vue'), meta: { title: 'Cookie Policy' } }
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
});

router.onError((error, to) => {
  if (error.message.includes('Failed to fetch dynamically imported module') && window.navigator.onLine) {
    window.location = to.fullPath;
  }
});

export default router;