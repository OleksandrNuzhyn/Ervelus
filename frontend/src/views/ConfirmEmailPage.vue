<template>
  <div class="background-container flex items-center justify-center">
    <div class="w-full max-w-md">
      <ConfirmEmailForm />
    </div>
  </div>
</template>


<script setup>
import ConfirmEmailForm from '@/components/AuthComponents/ConfirmEmailForm.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/light_leak.webp');
  min-height: 100vh;
  background-position: center;
  background-size: cover;
}
</style>