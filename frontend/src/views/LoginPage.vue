<template>
  <div class="background-container">
    <div class="min-h-screen flex items-stretch justify-end">
      <div class="w-full md:w-[32rem]">
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
  background-image: url('@/assets/register.jpg');
  background-size: cover;
  background-position: left center;
  min-height: 100vh;
}
</style>
