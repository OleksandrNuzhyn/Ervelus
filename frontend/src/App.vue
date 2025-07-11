<template>
  <div id="app" class="min-h-screen w-full bg-gray-900 text-white">
    <RouterView />
  </div>
</template>

  <script setup>
  import { onMounted } from 'vue';
  import { RouterView } from 'vue-router';
  import { useAuthStore } from '@/stores/auth';

  onMounted(async () => {
    const authStore = useAuthStore();
    try {
      await authStore.checkAuth();
    } 
    catch (error) {
      console.error("Error during initial auth check in App.vue:", error);
    }
  });
  </script>