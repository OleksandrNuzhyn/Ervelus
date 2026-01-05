<template>
  <div class="background-container w-full flex flex-col">
    <div class="flex items-stretch justify-end flex-1">
      <div class="w-full md:w-[32rem]">
        <ConfirmEmailForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import ConfirmEmailForm from '@/components/AuthComponents/ConfirmEmailForm.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/register.webp');
  min-height: 100vh;
  background-position: center center;
  background-size: cover;
}
</style>