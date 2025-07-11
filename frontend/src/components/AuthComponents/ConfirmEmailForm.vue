<template>
  <div class="w-full max-w-md p-8 space-y-6 bg-gradient-to-b from-purple-965 via-purple-900 to-indigo-900 rounded-xl shadow-2xl text-gray-300 font-serif">
    
    <div class="text-center">
      <h2 class="text-3xl font-bold text-white">Email Confirmation</h2>
      <p class="mt-2 text-gray-400">Please wait while we verify your email address.</p>
    </div>

    <div v-if="loading" class="text-center py-4">
      <p class="text-lg text-orange-400 animate-pulse">Verifying you...</p>
    </div>

    <div v-if="error" class="p-4 bg-red-900 border border-red-700 rounded-md text-center">
      <p class="font-bold text-red-300">Verification Failed</p>
      <p class="text-red-400">{{ error }}</p>
    </div>

    <div v-if="success" class="p-4 bg-green-900 border border-green-700 rounded-md text-center">
      <p class="font-bold text-green-300">Greetings Traveller!</p>
      <p class="text-green-400">Your email has been confirmed. Redirecting to the dashboard...</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const loading = ref(false);
const success = ref(false);
const error = ref(null);

onMounted(async () => {
  const { token } = route.params;

  if (!token) {
    error.value = 'Verification token was not found in the URL.';
    return;
  }

  loading.value = true;
  error.value = null;
  success.value = false;

  try {
    await api.post('/api/auth/registration/verify-email/', { key: token });
    success.value = true;
    
    await authStore.checkAuth();
    
    setTimeout(() => {
      router.push('/dashboard');
    }, 2000);

  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
        error.value = err.response.data.detail;
    } else {
        error.value = 'The token is invalid or has expired. Please try again.';
    }
    console.error('Email confirmation failed:', err);
  } finally {
    loading.value = false;
  }
});
</script>
