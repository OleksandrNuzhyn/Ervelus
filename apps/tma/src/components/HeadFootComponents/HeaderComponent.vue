<template>
  <header class="fixed inset-x-0 top-0 z-50 bg-black/30 backdrop-blur-sm">
    <div class="max-w-screen mx-auto px-4 sm:px-6 lg:px-12">
      <div class="flex items-center justify-between h-[70px]">
        <router-link to="/" class="flex items-center gap-3 text-2xl font-bold text-gray-100 select-none mobile-up">
          <img src="/favicon.svg" alt="Ervelus Logo" class="h-10 w-10" />
          <span>Ervelus</span>
        </router-link>
        <div class="flex items-center gap-3">
          <button @click="isBurgerOpen = !isBurgerOpen" class="text-gray-200 hover:text-gray-50 focus:outline-none">
            <svg v-if="!isBurgerOpen" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="transform opacity-0 -translate-y-4"
      enter-to-class="transform opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="transform opacity-100 translate-y-0"
      leave-to-class="transform opacity-0 -translate-y-4">
      <div v-if="isBurgerOpen" class="bg-black/30 backdrop-blur-sm text-gray-200">
        <div class="px-4 py-4 flex flex-col gap-6">
          <div class="flex items-center gap-2 text-gray-100">
            <div class="w-10 flex justify-center">
              <img src="@/assets/svg/coin.svg" class="h-10 w-10" style="filter: brightness(0) invert(1);" />
            </div>
            <span>{{ $t('navigation.coins') }}: {{ credits }}</span>
          </div>
          <router-link to="/" class="hover:text-gray-50 flex items-center gap-2">
            <div class="w-10 flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span>{{ $t('navigation.dashboard') }}</span>
          </router-link>
          <router-link to="/gallery" class="hover:text-white flex items-center gap-2">
            <div class="w-10 flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span>{{ $t('navigation.gallery') }}</span>
          </router-link>
          <router-link to="/profile" class="hover:text-white flex items-center gap-2">
            <div class="w-10 flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span>{{ $t('navigation.profile') }}</span>
          </router-link>
        </div>
      </div>
    </transition>
  </header>
  
  <transition
    enter-active-class="transition-opacity ease-in-out duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity ease-in-out duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="isBurgerOpen"
      @click="isBurgerOpen = false"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40">
    </div>
  </transition>
</template>
  
<script setup>
import { ref, watch } from 'vue';
import api from '@/services/api';

const isBurgerOpen = ref(false);
const credits = ref(0);

async function fetchCredits() {
  try {
    const response = await api.get('/api/auth/credit-balance/');
    credits.value = response.data.total_credits;
  }
  catch (error) {
    credits.value = 0;
  }
}

watch(isBurgerOpen, (newValue) => {
  if (newValue) {
    fetchCredits();
  }
});
</script>

<style scoped>
@media (max-width: 767px) {
  .mobile-up {
    position: relative;
    top: -2px;
  }
}
</style>