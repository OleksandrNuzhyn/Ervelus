<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-xs p-8 space-y-6 bg-white rounded-lg shadow-md">
      <h2 class="text-2xl font-bold text-center text-gray-800">Dashboard</h2>
      <LogoutForm />
    </div>
  </div>
</template>

<script setup>
import LogoutForm from '@/components/AuthComponents/LogoutForm.vue';
</script> 