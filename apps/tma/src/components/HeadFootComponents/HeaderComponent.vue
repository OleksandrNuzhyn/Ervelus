<template>
  <header 
    class="fixed inset-x-0 top-0 z-[70] transition-all duration-300"
    :class="isBurgerOpen ? 'bg-black/60 backdrop-blur-md shadow-2xl' : 'bg-black/30 backdrop-blur-sm'"
  >
    <div class="max-w-screen mx-auto px-4 sm:px-6 lg:px-12">
      <div class="flex items-center justify-between h-[70px]">
        <router-link to="/" class="flex items-center gap-3 text-2xl font-bold text-gray-100 select-none mobile-up">
          <img src="/favicon.svg" alt="Ervelus Logo" class="h-10 w-10" />
          <span>Ervelus</span>
        </router-link>
        <div class="flex items-center gap-3">
          <button @click="isStoreOpen = true" class="relative text-gray-200 hover:text-white transition-colors focus:outline-none mr-1">
            <div class="relative">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-7 w-7">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
              <div class="absolute -bottom-1 -right-1">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 15" fill="currentColor" class="w-3.5 h-3.5 text-yellow-400" style="filter: drop-shadow(0px 0px 3px rgba(0,0,0,1));">
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M6.63869 12.1902L3.50621 14.1092C3.18049 14.3087 2.75468 14.2064 2.55515 13.8807C2.45769 13.7216 2.42864 13.5299 2.47457 13.3491L2.95948 11.4405C3.13452 10.7515 3.60599 10.1756 4.24682 9.86791L7.6642 8.22716C7.82352 8.15067 7.89067 7.95951 7.81418 7.80019C7.75223 7.67116 7.61214 7.59896 7.47111 7.62338L3.66713 8.28194C2.89387 8.41581 2.1009 8.20228 1.49941 7.69823L0.297703 6.69116C0.00493565 6.44581 -0.0335059 6.00958 0.211842 5.71682C0.33117 5.57442 0.502766 5.48602 0.687982 5.47153L4.35956 5.18419C4.61895 5.16389 4.845 4.99974 4.94458 4.75937L6.36101 1.3402C6.5072 0.987302 6.91179 0.819734 7.26469 0.965925C7.43413 1.03612 7.56876 1.17075 7.63896 1.3402L9.05539 4.75937C9.15496 4.99974 9.38101 5.16389 9.6404 5.18419L13.3322 5.47311C13.713 5.50291 13.9975 5.83578 13.9677 6.2166C13.9534 6.39979 13.8667 6.56975 13.7269 6.68896L10.9114 9.08928C10.7131 9.25826 10.6267 9.52425 10.6876 9.77748L11.5532 13.3733C11.6426 13.7447 11.414 14.1182 11.0427 14.2076C10.8642 14.2506 10.676 14.2208 10.5195 14.1249L7.36128 12.1902C7.13956 12.0544 6.8604 12.0544 6.63869 12.1902Z" fill="currentColor"></path>
                </svg>
              </div>
            </div>
          </button>
          <button @click="isBurgerOpen = !isBurgerOpen" class="text-gray-200 hover:text-gray-50 focus:outline-none translate-y-[2px]">
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
      <div v-if="isBurgerOpen" class="text-gray-200">
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
    <StoreModal :isOpen="isStoreOpen" @close="isStoreOpen = false" />
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
      class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[65]">
    </div>
  </transition>
</template>
  
<script setup>
import { ref, watch, onUnmounted } from 'vue';
import api from '@/services/api';
import StoreModal from '@/components/OtherComponents/StoreModal.vue';

const isBurgerOpen = ref(false);
const isStoreOpen = ref(false);
const credits = ref(0);

const closeStore = () => {
  isStoreOpen.value = false;
};

watch(isStoreOpen, (val) => {
  const tg = window.Telegram?.WebApp;
  if (val) {
    tg?.BackButton.show();
    tg?.BackButton.onClick(closeStore);
  }
  else {
    tg?.BackButton.offClick(closeStore);
    tg?.BackButton.hide();
  }
});

async function fetchCredits() {
  try {
    const response = await api.get('/api/users/credit-balance/');
    credits.value = response.data.credits;
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

onUnmounted(() => {
  const tg = window.Telegram?.WebApp;
  tg?.BackButton.offClick(closeStore);
});
</script>