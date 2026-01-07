<template>
  <div class="form-container space-y-6 text-gray-300">
    <div v-if="isLoading" class="text-center py-4">
      <p class="text-m text-gray-300 animate-pulse">Verifying you...</p>
    </div>

    <div v-if="error" class="text-center">
      <p class="font-bold text-red-500">Verification Failed</p>
      <p class="text-gray-300">{{ error }}</p>
    </div>

    <div v-if="success" class="text-center space-y-1">
      <p class="font-bold text-green-300">Greetings Traveller!</p>
      <p class="text-gray-300">Your email has been confirmed. Redirecting to the dashboard...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const isLoading = ref(false);
const success = ref(false);
const error = ref(null);

async function verifyToken(token) {
  if (!token) {
    error.value = 'Verification token was not found in the URL';
    return;
  }

  isLoading.value = true;
  error.value = null;
  success.value = false;

  try {
    const response = await api.post('/api/auth/registration/verify-email/', { key: token });
    const authToken = response.data.key;

    if (authToken) {
      localStorage.setItem('user-token', authToken);
    }
    
    isLoading.value = false;
    success.value = true;
    
    await authStore.checkAuth();
    
    setTimeout(() => {
      router.push('/dashboard');
    }, 1000);

  } 
  catch (err) {
    if (err.response) {
      error.value = err.response.data?.detail || 'The token is invalid or has expired. Please try again';
    }
  } 
  finally {
    isLoading.value = false;
  }
};

watch(
  () => route.params.token,
  async (newToken) => {
    if (newToken) {
      await verifyToken(newToken);
    }
  },
  { immediate: true }
);
</script>

<style scoped>
.form-container {
  height: 100%;
  margin-left: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: rgba(10, 10, 10, 0.3) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 2rem;
  font-family: 'Manrope', sans-serif;
  color: #e5e7eb;
}
</style>