<template>
  <div class="background-container">
    <div class="min-h-screen flex items-stretch justify-end">
      <div class="w-[40%]">
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
  background-image: url('@/assets/register.png');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
}
</style>
