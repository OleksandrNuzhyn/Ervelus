<template>
  <div>
    <HeaderComponent />
    <div class="background-container w-full flex items-stretch pt-20">
      <div class="w-full">
        <GalleryComponent />
      </div>
    </div>
  </div>
</template>

<script setup>
import HeaderComponent from '@/components/OtherComponents/HeaderComponent.vue'
import GalleryComponent from '@/components/GalleryComponents/GalleryComponent.vue'
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/gallery.webp');
  min-height: max(100vh, calc(100vw * 23 / 48));
  background-size: cover;
  background-position: 48.4% bottom;
  background-attachment: fixed;
}
</style>