<template>
  <div class="background-container flex items-center justify-center">
    <div class="w-full max-w-sm px-4">
      <ResetPasswordConfirm />
    </div>
  </div>
</template>

<script setup>
import ResetPasswordConfirm from '@/components/AuthComponents/ResetPasswordConfirmForm.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/side_background.webp');
  min-height: 100vh;
  background-position: center;
  background-size: cover;
}
</style> 