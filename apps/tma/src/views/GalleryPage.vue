<template>
  <div>
    <HeaderComponent />
    <div class="page-bg w-full flex items-stretch pt-20">
      <div class="noise-overlay"></div>
      <div class="ambient-light"></div>
      <div class="global-background">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="glow-orb orb-3"></div>
        <div class="grid-overlay"></div>
      </div>
      <div class="w-full relative z-10">
        <GalleryComponent />
      </div>
    </div>
  </div>
</template>

<script setup>
import HeaderComponent from '@/components/OtherComponents/HeaderComponent.vue'
import GalleryComponent from '@/components/GalleryComponents/GalleryComponent.vue'
</script>