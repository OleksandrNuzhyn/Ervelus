<template>
  <div id="app" class="min-h-screen w-full bg-gray-900 text-white">
    <RouterView v-if="authStore.authChecked" />
    <div v-else class="flex h-screen items-center justify-center">
      <p>Завантаження...</p>
    </div>
  </div>
</template>

<script setup>

import { RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

</script>