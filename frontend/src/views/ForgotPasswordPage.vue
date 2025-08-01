<template>
  <div class="background-container flex items-center justify-center">
    <div class="w-full max-w-sm">
      <ForgotPasswordForm />
    </div>
  </div>
</template>

<script setup>
import ForgotPasswordForm from '@/components/AuthComponents/ForgotPasswordForm.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/light_leak.webp');
  min-height: 100vh;
  background-position: center;
  background-size: cover;
}
</style> 