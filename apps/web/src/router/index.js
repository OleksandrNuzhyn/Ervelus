import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomePage.vue'), meta: { title: 'Ervelus' } },
  { path: '/terms-of-service', name: 'terms-of-service', component: () => import('@/views/TermsOfServicePage.vue'), meta: { title: 'Terms of Service' } },
  { path: '/privacy-policy', name: 'privacy-policy', component: () => import('@/views/PrivacyPolicyPage.vue'), meta: { title: 'Privacy Policy' } },
  { path: '/refund-policy', name: 'refund-policy', component: () => import('@/views/RefundPolicyPage.vue'), meta: { title: 'Refund Policy' } },
  { path: '/cookie-policy', name: 'cookie-policy', component: () => import('@/views/CookiePolicyPage.vue'), meta: { title: 'Cookie Policy' } },
  { path: '/about-us', name: 'about-us', component: () => import('@/views/AboutUsPage.vue'), meta: { title: 'About Us' } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from) => {
  document.title = to.meta.title || 'Ervelus';
});

router.onError((error, to) => {
  if (error.message.includes('Failed to fetch dynamically imported module') && window.navigator.onLine) {
    window.location = to.fullPath;
  }
});

export default router;