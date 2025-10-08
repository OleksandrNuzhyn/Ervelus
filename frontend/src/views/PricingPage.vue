<template>
  <div>
    <HeaderComponent />
    <div class="background-container pt-20">
      <PricingComponent />
    </div>
    <FooterComponent />
  </div>
</template>

<script setup>
import PricingComponent from '@/components/PricingComponent.vue';
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue';
import FooterComponent from '@/components/HeadFootComponents/FooterComponent.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/wall.webp');
  background-size: cover;
  background-position: top center;
  background-attachment: fixed;
  min-height: max(100vh, calc(100vw * 23 / 48));
}
</style>