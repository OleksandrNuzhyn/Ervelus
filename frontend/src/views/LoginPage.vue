<template>
  <div class="background-container w-full flex items-stretch justify-end">
    <div class="w-full md:w-[32rem]">
      <LoginForm />
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
