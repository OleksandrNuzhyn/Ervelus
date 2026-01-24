<template>
  <div>
    <HeaderComponent />
    <div class="background-container w-full flex items-stretch pt-[82px]">
      <div class="w-full">
        <ProfileComponent />
      </div>
    </div>
  </div>
</template>
  
<script setup>
import ProfileComponent from '@/components/OtherComponents/ProfileComponent.vue';
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue';
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/side_background.webp');
  min-height: max(100vh, calc(100vw * 23 / 48));
  background-size: cover;
  background-position: left top;
  background-attachment: fixed;
}
</style>