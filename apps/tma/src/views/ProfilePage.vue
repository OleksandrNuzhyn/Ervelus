<template>
  <div>
    <HeaderComponent />
    <div class="page-bg w-full flex items-stretch pt-[82px]">
      <div class="noise-overlay"></div>
      <div class="ambient-light"></div>
      <div class="global-background">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="glow-orb orb-3"></div>
        <div class="grid-overlay"></div>
      </div>
      <div class="w-full relative z-10">
        <ProfileComponent />
      </div>
    </div>
  </div>
</template>
  
<script setup>
import ProfileComponent from '@/components/OtherComponents/ProfileComponent.vue';
import HeaderComponent from '@/components/OtherComponents/HeaderComponent.vue';
</script>