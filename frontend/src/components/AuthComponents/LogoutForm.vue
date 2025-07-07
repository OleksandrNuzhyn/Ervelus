<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900 text-white">
    <div class="w-full max-w-md p-8 space-y-6 bg-gradient-to-b from-purple-965 via-purple-950 to-indigo-980 rounded-xl shadow-2xl text-center">
      <h2 class="text-3xl font-bold text-white">Confirm Logout</h2>
      <p class="text-gray-400">Are you sure you want to end your session?</p>
      
      <div class="flex justify-center space-x-4">
        <button
          @click="handleLogout"
          :disabled="isLoading"
          class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading">Logging out...</span>
          <span v-else>Confirm Logout</span>
        </button>
        <button
          @click="router.back()"
          class="w-full py-3 font-bold text-gray-300 bg-gray-700 rounded-md hover:bg-gray-600 transition duration-300"
        >
          Cancel
        </button>
      </div>
    </div>
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

async function handleLogout() {
  isLoading.value = true;
  try {
    await api.post('api/auth/logout/');
  } 
  catch (error) {
    console.error('Backend logout failed, proceeding with client-side logout:', error);
  } 
  finally {
    authStore.$reset();
    router.push({ name: 'login' });
    isLoading.value = false;
  }
}
</script>