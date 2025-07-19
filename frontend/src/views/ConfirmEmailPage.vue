<template>
  <div class="background-container min-h-screen flex items-center justify-center">
    <ConfirmEmailForm />
  </div>
</template>

<script setup>
import ConfirmEmailForm from '@/components/AuthComponents/ConfirmEmailForm.vue';
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