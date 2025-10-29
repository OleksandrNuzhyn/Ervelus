<template>
  <div>
    <HeaderComponent />
    <div class="background-container flex items-center justify-center">
      <ContactUsComponent />
    </div>
    <FooterComponent />
  </div>
</template>

<script setup>
import ContactUsComponent from '@/components/OtherComponents/ContactUsComponent.vue';
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue';
import FooterComponent from '@/components/HeadFootComponents/FooterComponent.vue';
</script> 

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/wall.webp');
  background-size: cover;
  background-position: top center;
  min-height: max(100vh, calc(100vw * 23 / 48));
}
</style>