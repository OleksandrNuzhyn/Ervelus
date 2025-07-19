<template>
  <div class="form-container w-full max-w-md space-y-6 text-gray-300">
      
      <div class="text-center">
        <h2 class="text-2xl font-bold text-white">Email Confirmation</h2>
        <p class="mt-2 text-gray-300">Please wait while we verify your email address</p>
      </div>

      <div v-if="isLoading" class="text-center py-4">
        <p class="text-m text-gray-300 animate-pulse">Verifying you...</p>
      </div>

      <div v-if="error" class="p-4 bg-red-900 border border-red-700 rounded-md text-center">
        <p class="font-bold text-red-300">Verification Failed</p>
        <p class="text-red-400">{{ error }}</p>
      </div>

      <div v-if="success" class="text-center space-y-1">
        <p class="font-bold text-green-300">Greetings Traveller!</p>
        <p class="text-gray-300">Your email has been confirmed. Redirecting to the dashboard...</p>
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

const isLoading = ref(false);
const success = ref(false);
const error = ref(null);

onMounted(async () => {
  const { token } = route.params;

  if (!token) {
    error.value = 'Verification token was not found in the URL.';
    return;
  }

  isLoading.value = true;
  error.value = null;
  success.value = false;

  try {
    await api.post('/api/auth/registration/verify-email/', { key: token });
    success.value = true;
    
    await authStore.checkAuth();
    
    setTimeout(() => {
      router.push('/dashboard');
    }, 3000);

  } 
  catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
        error.value = err.response.data.detail;
    } 
    else {
        error.value = 'The token is invalid or has expired. Please try again.';
    }
  } 
  finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: rgba(10, 10, 10, 0.3) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 2rem;
  font-family: 'Manrope', sans-serif;
  color: #e5e7eb;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
}
</style>