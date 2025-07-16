<template>
  <div class="background-container">
    <div class="min-h-screen flex items-stretch justify-end">
      <div class="w-[40%]">
        <RegisterForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import RegisterForm from '@/components/AuthComponents/RegisterForm.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/register.jpg');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
}
</style>