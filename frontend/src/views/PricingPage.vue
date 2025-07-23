<template>
  <div class="background-container">
    <PricingComponent />
  </div>
</template>

<script setup>
import PricingComponent from '@/components/PricingComponent.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/wall.webp');
  background-size: cover;
  background-position: top center;
  min-height: max(100vh, calc(100vw * 23 / 48));
}
</style>
