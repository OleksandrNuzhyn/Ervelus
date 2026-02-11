<template>
  <div>
    <HeaderComponent />
    <div class="w-full flex items-stretch pt-[82px]">
      <div class="w-full">
        <ProfileComponent />
      </div>
    </div>
  </div>
</template>
  
<script setup>
import ProfileComponent from '@/components/OtherComponents/ProfileComponent.vue';
import HeaderComponent from '@/components/OtherComponents/HeaderComponent.vue';
</script>