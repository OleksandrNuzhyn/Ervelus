<template>
  <div v-if="!isLoading" class="background-container w-full flex flex-col">
    <div class="flex items-stretch justify-end flex-1">
      <div class="w-full md:w-[32rem]">
        <RegisterForm v-if="isRegistrationEnabled" />
        <RegistrationUnavailableComponent v-else />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import RegisterForm from '@/components/AuthComponents/RegisterForm.vue';
import RegistrationUnavailableComponent from '@/components/AuthComponents/RegistrationUnavailableComponent.vue';
import api from '@/services/api';

const isRegistrationEnabled = ref(true);
const isLoading = ref(true);

async function getApplicationConfig() {
  try {
    const response = await api.get('/api/core/app-config/');
    isRegistrationEnabled.value = response.data.is_registration_enabled;
  }
  catch {
    isRegistrationEnabled.value = true;
  }
  finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  getApplicationConfig();
});
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background_assets/register.webp');
  min-height: max(100vh, calc(100vw * 23 / 48));
  background-size: cover;
  background-position: left top;
}
</style>