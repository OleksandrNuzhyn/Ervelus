<template>
  <div class="background-container w-full flex flex-col">
    <div class="absolute top-6 left-6 md:left-12 z-10">
      <router-link to="/" class="text-2xl font-bold text-white hover:text-gray-300 transition-colors select-none">
        Ervelus
      </router-link>
    </div>
    <div class="flex items-stretch justify-end flex-1">
      <div class="w-full md:w-[32rem]">
        <LoginForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import LoginForm from '@/components/AuthComponents/LoginForm.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/register.webp');
  min-height: max(100vh, calc(100vw * 23 / 48));
  background-size: cover;
  background-position: left top;
}
</style>
