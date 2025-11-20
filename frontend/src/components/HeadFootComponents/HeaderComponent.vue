<template>
  <header class="fixed inset-x-0 top-0 z-50 bg-black/30 backdrop-blur-sm">
    <div class="max-w-screen mx-auto px-4 sm:px-6 lg:px-12">
      <div class="flex items-center justify-between h-[70px]">
        <router-link to="/" class="flex items-center gap-3 text-2xl font-bold text-gray-100 select-none">
          <img src="/favicon.svg" alt="Ervelus Logo" class="h-10 w-10" />
          <span>Ervelus</span>
        </router-link>
        <nav v-if="authStore.isAuthenticated" class="hidden md:flex items-center gap-15 font-thin text-gray-100">
          <router-link to="/dashboard" class="hover:text-gray-400">Dashboard</router-link>
          <router-link to="/gallery" class="hover:text-gray-400">Gallery</router-link>
          <router-link to="/pricing" class="hover:text-gray-400">Pricing</router-link>
          <SideBarComponent
            ref="sideBar"
            :credits="credits"
            @open-change="handleBarChange"
            @logout="handleLogout"
          />
        </nav>
        <button v-if="authStore.isAuthenticated" @click="isBurgerOpen = !isBurgerOpen" class="md:hidden text-gray-200 hover:text-gray-50 focus:outline-none">
          <svg v-if="!isBurgerOpen" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div v-else class="flex items-center gap-15 font-thin text-gray-100">
          <router-link to="/pricing" class="hidden md:block hover:text-gray-400">Pricing</router-link>
          <router-link to="/contact-us" class="hidden md:block hover:text-gray-400">Contact us</router-link>
          <div class="flex items-center gap-5">
            <router-link to="/register" class="rounded-full px-4 py-2 text-gray-100 transition-all duration-300" style="background: #8b5cf6; box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);">Enter Ervelus</router-link>
            <button @click="isGuestBurgerOpen = !isGuestBurgerOpen" class="md:hidden text-gray-200 hover:text-gray-50 focus:outline-none">
              <svg v-if="!isGuestBurgerOpen" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
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
      <div v-if="isBurgerOpen" class="md:hidden bg-black/30 backdrop-blur-sm text-gray-200">
        <div class="px-4 py-4 flex flex-col gap-6">
            <div class="py-3 text-sm text-gray-400 flex items-center gap-2">
              <div class="w-10 flex justify-center">
                <img src="@/assets/svg/coin.svg" class="h-10 w-10" />
              </div>
              <span>COINS: {{ credits }}</span>
            </div>
            <router-link to="/dashboard" class="hover:text-gray-50 flex items-center gap-2">
              <div class="w-10 flex justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span>Dashboard</span>
            </router-link>
            <router-link to="/gallery" class="hover:text-white flex items-center gap-2">
              <div class="w-10 flex justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span>Gallery</span>
            </router-link>
            <router-link to="/profile" class="hover:text-white flex items-center gap-2">
              <div class="w-10 flex justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span>Profile</span>
            </router-link>
            <router-link to="/pricing" class="hover:text-gray-50 flex items-center gap-2">
              <div class="w-10 flex justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span>Pricing</span>
            </router-link>
            <router-link to="/contact-us" @click="isBarOpen = false" class="hover:text-white flex items-center gap-2">
              <div class="w-10 flex justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z"/>
                </svg>
              </div>
              <span>Contact us</span>
            </router-link>
            <button @click="handleLogout" class="text-left hover:text-white flex items-center gap-2">
              <div class="w-10 flex justify-center">
                <svg class="w-9 h-9" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20V9.75a5 5 0 00-10 0V20M2 20h20"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 12h8m0 0l-3-3m3 3l-3 3"></path></svg>
              </div>
              <span>Sign out</span>
            </button>
          </div>
        </div>
      </transition>

    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="transform opacity-0 -translate-y-4"
      enter-to-class="transform opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="transform opacity-100 translate-y-0"
      leave-to-class="transform opacity-0 -translate-y-4">
      <div v-if="isGuestBurgerOpen" class="md:hidden bg-black/30 backdrop-blur-sm text-gray-200">
        <div class="px-4 py-4 flex flex-col gap-6">
          <router-link to="/pricing" @click="isGuestBurgerOpen = false" class="hover:text-gray-50 flex items-center gap-2">
            <div class="w-10 flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span>Pricing</span>
          </router-link>
          <router-link to="/contact-us" @click="isGuestBurgerOpen = false" class="hover:text-white flex items-center gap-2">
            <div class="w-10 flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z"/>
              </svg>
            </div>
            <span>Contact us</span>
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
      v-if="isBarOpen || isBurgerOpen || isGuestBurgerOpen"
      @click="closeSidebars"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40">
    </div>
  </transition>
</template>
  
<script setup>
import { ref, watch } from 'vue';
import SideBarComponent from './SideBarComponent.vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { toast } from '@/services/toast';

const isBurgerOpen = ref(false);
const isGuestBurgerOpen = ref(false);
const isBarOpen = ref(false);
const credits = ref(0);
const sideBar = ref(null);

const authStore = useAuthStore();
const router = useRouter();

function closeSidebars() {
  if (sideBar.value) {
    sideBar.value.closeBar();
  }

  isBarOpen.value = false;
  isBurgerOpen.value = false;
  isGuestBurgerOpen.value = false;
}

async function fetchCredits() {
  if (!authStore.isAuthenticated) return;
  try {
    const response = await api.get('/api/auth/credit-balance/');
    credits.value = response.data.total_credits;
  }
  catch (error) {
    credits.value = 0;
  }
}

function handleBarChange(newValue) {
  isBarOpen.value = newValue;

  if (newValue) {
    fetchCredits();
  }
}

async function handleLogout() {
  try {
    await authStore.logout();
    router.push({ name: 'login' });
  }
  catch (error) {
    toast.info('Could not sign out. Please try again');
  }
  finally {
    closeSidebars();
  }
}

watch(isBurgerOpen, (newValue) => {
  if (newValue) {
    fetchCredits();
  }
});
</script> 