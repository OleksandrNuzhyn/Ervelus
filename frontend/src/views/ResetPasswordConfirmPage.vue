<template>
  <div class="background-container min-h-screen flex items-center justify-center">
    <ResetPasswordConfirm />
  </div>
</template>

<script setup>
import ResetPasswordConfirm from '@/components/AuthComponents/ResetPasswordConfirm.vue';
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