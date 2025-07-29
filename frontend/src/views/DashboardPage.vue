<template>
  <div class="dashboard-background">
    <div class="flex items-center justify-center min-h-screen bg-transparent">
      <div class="w-full max-w-xs p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h2 class="text-2xl font-bold text-center text-gray-800">Dashboard</h2>
        <WebPortalComponent />
        <LogoutForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import LogoutForm from '@/components/AuthComponents/LogoutForm.vue';
import WebPortalComponent from '@/components/WebPortalComponent.vue';
</script>

<style scoped>
.dashboard-background {
  background-image: url('@/assets/test.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
}
</style> 