<template>
  <HeaderComponent />
  <div class="background-container min-h-screen text-white flex justify-center items-start pt-15">
    <main class="w-full mx-auto px-4 sm:px-6 lg:px-8 xl:px-35">
      <GenerationComponent />
    </main>
  </div>
</template>

<script setup>
import GenerationComponent from '@/components/GenerationComponents/GenerationComponent.vue';
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/sky_star.png');
  background-size: cover;
  background-position: top center;
  min-height: max(100vh, calc(100vw * 23 / 48));
}
</style>