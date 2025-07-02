<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-50">
    <h1 class="text-4xl font-bold mb-4">Ласкаво просимо до Ervelus</h1>
    <p class="text-lg mb-8">Будь ласка, увійдіться або зареєструйтесь, щоб продовжити.</p>
    <div class="flex space-x-4">
      <router-link to="/login" class="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Увійти</router-link>
      <router-link to="/register" class="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600">Зареєструватися</router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const router = useRouter();

onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/dashboard');
  }
});
</script> 