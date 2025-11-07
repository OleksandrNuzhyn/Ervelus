<template>
  <div class="flex flex-col min-h-screen">
    <HeaderComponent />
    <main class="flex-grow pt-20 pb-10 flex flex-col">
      <div v-if="document.content" class="document-container">
        <div v-html="document.content" class="document-content"></div>
      </div>
      <div v-else-if="errorMessage" class="flex-grow flex flex-col items-center justify-center text-center">
        <h1 class="text-3xl font-bold text-white">{{ document.title }}</h1>
        <p class="mt-4 text-gray-300">{{ errorMessage }}</p>
      </div>
    </main>
    <FooterComponent v-if="isContentLoaded" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api.js';
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue';
import FooterComponent from '@/components/HeadFootComponents/FooterComponent.vue';

const document = ref({
  title: 'Privacy Policy',
  content: ''
});
const errorMessage = ref(null);
const isContentLoaded = ref(false);

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
  finally {
    isContentLoaded.value = true;
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