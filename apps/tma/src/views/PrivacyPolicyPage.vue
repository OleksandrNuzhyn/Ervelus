<template>
  <div class="flex flex-col min-h-screen">
    <div class="noise-overlay"></div>
    <div class="ambient-light"></div>
    <div class="global-background">
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
      <div class="glow-orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>
    <HeaderComponent />
    <main class="flex-grow pt-[70px] pb-10 flex flex-col relative z-20">
      <div class="pt-8 pb-4 flex justify-end px-8 max-w-[800px] mx-auto w-full text-right">
        <button 
          v-if="canGoBack"
          @click="goBack" 
          class="group flex items-center gap-2 px-3 py-2 rounded-2xl bg-white/5 hover:bg-white/10 border border-white/[0.02] active:scale-95 transition-all w-fit backdrop-blur-sm"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-white/60 group-hover:text-white group-hover:-translate-x-0.5 transition-all">
            <path d="M19 12H5"/>
            <path d="M12 19l-7-7 7-7"/>
          </svg>
          <span class="text-sm font-medium text-white/60 group-hover:text-white transition-colors">{{ $t('navigation.back') || 'Back' }}</span>
        </button>
      </div>
      <div v-if="document.content" class="document-container !pt-0" @click="handleContentClick">
        <div v-html="document.content" class="document-content"></div>
      </div>
      <div v-else-if="errorMessage" class="flex-grow flex flex-col items-center justify-center text-center">
        <h1 class="text-3xl font-bold text-white">{{ document.title }}</h1>
        <p class="mt-4 text-gray-300">{{ errorMessage }}</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api.js';
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue';

const router = useRouter();
const document = ref({
  title: 'Privacy Policy',
  content: ''
});
const errorMessage = ref(null);
const canGoBack = computed(() => window.history.state.back !== null);

function goBack() {
  router.back();
}

function handleContentClick(event) {
  const anchor = event.target.closest('a');
  const href = anchor?.getAttribute('href');

  if (anchor && href?.startsWith('#')) {
    event.preventDefault();
    const elementId = href.substring(1);

    if (elementId) {
      const targetElement = window.document.getElementById(elementId);
      
      if (targetElement) {
        const headerOffset = 75;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    }
  }
}

async function getDocument() {
  try {
    const response = await api.get('/api/agreements/privacy_policy/');
    document.value.content = response.data.content;
  }
  catch (error) {
    if (error.response && error.response.status === 404 && error.response.data.detail) {
      errorMessage.value = error.response.data.detail;
    }
    else {
      errorMessage.value = 'The document is currently unavailable. Please try again later';
    }
  }
}

onMounted(getDocument);
</script>

<style scoped>
.noise-overlay {
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
  opacity: 0.3;
  display: block;
}

.ambient-light {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 0%, rgba(139, 180, 255, 0.08), transparent 70%);
  pointer-events: none;
  z-index: 0;
  display: block; 
}

.global-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background-color: #0c0d14;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.2;
  mix-blend-mode: screen;
  display: block;
}

.orb-1 {
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  top: -200px;
  left: -200px;
  opacity: 1;
  filter: blur(80px); 
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: #94a3b8;
  bottom: -100px;
  right: -100px;
  opacity: 0.1;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.2);
  top: 40%;
  left: 40%;
  opacity: 0.1;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(circle at 50% 40%, black 60%, transparent 100%);
  opacity: 0.7;
  filter: brightness(1.7);
  display: block;
}
</style>

<style>
.document-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  color: #d1d5db;
}

.document-content {
  line-height: 1.6;
}

.document-content h1, .document-content h2, .document-content h3 {
  color: white;
  margin-bottom: 1rem;
}

.document-content h1 {
  font-size: 2.25rem;
  font-weight: bold;
  margin-top: 1.5rem;
}

.document-content h1:first-child {
  margin-top: 0;
}

.document-content h2 {
  font-size: 1.875rem;
  font-weight: bold;
  margin-top: 1.5rem;
}

.document-content h3 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 1.5rem;
}

.document-content p {
  margin-bottom: 1rem;
}

.document-content ul, .document-content ol {
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.document-content li {
  margin-bottom: 0.5rem;
}

.document-content a {
  color: #93c5fd;
  text-decoration: underline;
}

.document-content a:hover {
  color: #60a5fa;
}
</style>