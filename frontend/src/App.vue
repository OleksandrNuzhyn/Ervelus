<template>
    <div v-if="!authStore.isAuthReady" class="loading-overlay">
      <p>Завантаження...</p>
    </div>
    <RouterView v-else />
  </template>
  
  <script setup>
  import { RouterView } from 'vue-router'
  import { useAuthStore } from '@/stores/auth';
  const authStore = useAuthStore();
  </script>
  
  <style>
  .loading-overlay {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    inset: 0;
    background-color: #ffffff;
    z-index: 9999;
  }
  </style>