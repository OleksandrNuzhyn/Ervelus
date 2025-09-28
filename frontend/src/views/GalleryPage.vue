<template>
  <div class="flex flex-col">
    <HeaderComponent />

    <div class="background-container relative pt-20 lg:overflow-hidden">
      <!-- hide overlays on phones -->
      <!-- <div class="absolute inset-0 bg-black/30 hidden sm:block"></div> -->
      <!-- <div class="absolute inset-0 bg-gradient-to-b from-black/20 via-transparent to-black/40 hidden sm:block"></div> -->

      <div class="relative h-full">
        <GalleryComponent />
      </div>
    </div>
  </div>
</template>


<script setup>
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue'
import GalleryComponent from '@/components/GalleryComponents/GalleryComponent.vue'
</script>

<style scoped>
.background-container {
  /* MOBILE (default) */
  background-image: url('@/assets/background_assets/gallery_1_1.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;      /* fills screen, crops if needed */
  min-height: 100vh;
  height: auto;
  max-height: none;
  background-attachment: fixed;
}

/* Laptops/desktops (≥1024px) */
@media (min-width: 1024px) {
  .background-container {
    background-image: url('@/assets/background_assets/gallery_1.png');
  }
}
</style>





