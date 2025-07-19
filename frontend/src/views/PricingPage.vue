<template>
  <div class="background-container min-h-screen">
    <PricingComponent />
  </div>
</template>

<script setup>
import PricingComponent from '@/components/PricingComponent.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/light_leak.webp');
  background-position: center;
  background-size: cover;
}
</style>
