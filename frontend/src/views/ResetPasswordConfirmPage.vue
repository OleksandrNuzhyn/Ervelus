<template>
  <div class="background-container w-full flex flex-col">
    <div class="flex items-stretch justify-end flex-1">
      <div class="w-full md:w-[32rem]">
        <ResetPasswordConfirm />
      </div>
    </div>
  </div>
</template>

<script setup>
import ResetPasswordConfirm from '@/components/AuthComponents/ResetPasswordConfirmForm.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/register.webp');
  min-height: 100vh;
  background-size: cover;
  background-position: center center;
}
</style> 