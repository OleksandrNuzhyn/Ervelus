<template>
  <div>
    <button
      @click="handleLogout"
      :disabled="isLoading"
      class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed"
    >
      <span v-if="isLoading">Logging out...</span>
      <span v-else>Log Out</span>
    </button>
    <p v-if="error" class="mt-2 text-sm text-center text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';

const authStore = useAuthStore();
const router = useRouter();
const isLoading = ref(false);
const error = ref('');

async function handleLogout() {
  isLoading.value = true;
  error.value = '';
  try {
    await api.post('api/auth/logout/');
    authStore.$reset();
    await router.push({ name: 'login' });
  } 
  catch (err) {
    if (err.response) {
      const { status, data = {} } = err.response;
      if (status === 500) {
        error.value = data.detail || 'Server error, could not log out. Please try again.';
      } 
      else {
        error.value = 'An unexpected error occurred during logout.';
      }
    } 
    else {
      error.value = 'Network error. Please check your connection and try again.';
    }
  } 
  finally {
    isLoading.value = false;
  }
}
</script>