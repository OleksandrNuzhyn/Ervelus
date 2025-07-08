<template>
  <button
    @click="handleLogout"
    :disabled="isLoading"
    class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed"
  >
    <span v-if="isLoading">Logging out...</span>
    <span v-else>Log Out</span>
  </button>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';

const authStore = useAuthStore();
const router = useRouter();
const isLoading = ref(false);

async function handleLogout() {
  isLoading.value = true;
  try {
    await api.post('api/auth/logout/');
  } 
  catch (error) {
    console.error('Backend logout failed:', error);
  } 
  finally {
    authStore.$reset();
    router.push({ name: 'login' });
    isLoading.value = false;
  }
}
</script>