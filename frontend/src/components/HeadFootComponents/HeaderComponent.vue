<template>
    <header class="fixed inset-x-0 top-0 z-50 bg-black/30 backdrop-blur-sm">
      <div class="max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <router-link to="/" class="text-2xl font-bold text-gray-100 medieval select-none">Ervelus</router-link>
  
          <nav class="hidden md:flex items-center gap-6 text-gray-200">
            <router-link to="/dashboard" class="px-4 py-2 rounded bg-white/10 hover:bg-white/20 text-gray-100">Dashboard</router-link>
            <router-link to="/pricing" class="hover:text-gray-50">Pricing</router-link>
            <router-link to="/gallery" class="hover:text-gray-50">Gallery</router-link>
            <router-link to="/profile" class="hover:brightness-125">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 7.5a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.5 20.25a8.25 8.25 0 1115 0" />
              </svg>
            </router-link>
          </nav>
  
          <button @click="isOpen = !isOpen" class="md:hidden text-gray-200 hover:text-gray-50 focus:outline-none">
            <svg v-if="!isOpen" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
  
      <div v-if="isOpen" class="md:hidden bg-black/70 backdrop-blur-sm text-gray-200">
          <div class="px-4 py-4 flex flex-col gap-4">
            <router-link to="/dashboard" class="px-4 py-2 rounded bg-white/10 hover:bg-white/20 text-gray-100">Dashboard</router-link>
            <router-link to="/pricing" class="hover:text-gray-50">Pricing</router-link>
            <router-link to="/gallery" class="hover:text-gray-50">Gallery</router-link>
            <router-link to="/profile" class="hover:brightness-125 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 7.5a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.5 20.25a8.25 8.25 0 1115 0" />
              </svg>
              Profile
            </router-link>
          </div>
        </div>
    </header>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const isOpen = ref(false);
  </script> 