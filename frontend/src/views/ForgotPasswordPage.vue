<template>
  <div class="background-container min-h-screen flex items-center justify-center">
    <ForgotPasswordForm />
  </div>
</template>

<script setup>
import ForgotPasswordForm from '@/components/AuthComponents/ForgotPasswordForm.vue';
</script>

<style scoped>
.background-container {
  background-color: #111827;
  background-image: url('@/assets/light_leak.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}
</style> 