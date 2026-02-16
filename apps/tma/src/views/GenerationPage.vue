<template>
  <div>
    <HeaderComponent />
    <div class="page-bg min-h-screen text-white flex justify-center items-start pt-20">
      <div class="noise-overlay"></div>
      <div class="ambient-light"></div>
      <div class="global-background">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="glow-orb orb-3"></div>
        <div class="grid-overlay"></div>
      </div>
      <main class="w-full mx-auto px-4 sm:px-6 lg:px-8 xl:px-35 relative z-10">
        <GenerationComponent />
      </main>
    </div>
  </div>
</template>

<script setup>
import GenerationComponent from '@/components/GenerationComponents/GenerationComponent.vue';
import HeaderComponent from '@/components/OtherComponents/HeaderComponent.vue';
</script>