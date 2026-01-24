<template>
  <div class="flex flex-col min-h-screen">
    <HeaderComponent />
    <main class="flex-grow pt-24 pb-10 flex flex-col relative">
      <div class="px-8 max-w-[800px] mx-auto w-full mb-4">
        <button 
          @click="goBack" 
          class="group flex items-center gap-2 px-3 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 active:scale-95 transition-all w-fit backdrop-blur-sm"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-white/60 group-hover:text-white group-hover:-translate-x-0.5 transition-all">
            <path d="M19 12H5"/>
            <path d="M12 19l-7-7 7-7"/>
          </svg>
          <span class="text-sm font-medium text-white/60 group-hover:text-white transition-colors">{{ $t('gallery.prev') || 'Back' }}</span>
        </button>
      </div>
      <div v-if="document.content" class="document-container !pt-4" @click="handleContentClick">
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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api.js';
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue';

const router = useRouter();
const document = ref({
  title: 'Terms of Service',
  content: ''
});
const errorMessage = ref(null);

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
    const response = await api.get('/api/agreements/terms_of_service/');
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