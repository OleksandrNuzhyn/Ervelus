<template>
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="w-full max-w-7xl px-4 mx-auto sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex-shrink-0">
            <RouterLink to="/" class="text-xl font-bold text-gray-800 hover:text-blue-600">
              SaaS Project
            </RouterLink>
          </div>
  
          <nav class="hidden md:flex md:items-center md:space-x-8">
            <template v-if="authStore.isAuthenticated">
              <RouterLink to="/dashboard" class="font-medium text-gray-500 hover:text-gray-900">Дашборд</RouterLink>
              <RouterLink to="/settings" class="font-medium text-gray-500 hover:text-gray-900">Налаштування</RouterLink>
              <span class="text-sm text-gray-700">{{ authStore.user?.email }}</span>
              <button @click="authStore.logout()" class="text-sm font-medium text-gray-500 hover:text-gray-900">Вийти</button>
            </template>
            <template v-else>
              <RouterLink to="/login" class="text-base font-medium text-gray-500 hover:text-gray-900">Увійти</RouterLink>
              <RouterLink to="/register" class="ml-8 inline-flex items-center justify-center px-4 py-2 text-base font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700">
                Реєстрація
              </RouterLink>
            </template>
          </nav>
  
          <div class="md:hidden">
            <button type="button" class="p-2 text-gray-500 rounded-md hover:text-gray-700 hover:bg-gray-100">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router';
  import { useAuthStore } from '@/stores/auth';
  const authStore = useAuthStore();
  </script>