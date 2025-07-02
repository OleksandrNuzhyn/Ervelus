<template>
    <div class="flex flex-col min-h-screen bg-gray-50">
      <TheHeader />
      <main class="flex-grow w-full max-w-7xl px-4 py-8 mx-auto sm:px-6 lg:px-8">
        <RouterView />
      </main>
      <TheFooter />
    </div>
  </template>
  
  <script setup>
  import TheHeader from '@/components/TheHeader.vue';
  import TheFooter from '@/components/TheFooter.vue';
  import { RouterView } from 'vue-router';
  </script>