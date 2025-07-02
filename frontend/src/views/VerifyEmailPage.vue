<template>
    <AuthLayout>
      <div class="text-center">
        <h2 class="text-3xl font-extrabold text-center text-gray-100">Підтвердження Email</h2>
        <div class="mt-6">
          <BaseSpinner v-if="isLoading" class="mx-auto" />
          <AlertMessage :message="message" :type="isError ? 'error' : 'success'" />
        </div>
        <div v-if="!isLoading" class="mt-8">
          <RouterLink to="/login" class="font-medium text-purple-400 hover:text-purple-300">
            Перейти до сторінки входу
          </RouterLink>
        </div>
      </div>
    </AuthLayout>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import { RouterLink } from 'vue-router';
  import AuthLayout from '@/layouts/AuthLayout.vue';
  import BaseSpinner from '@/components/ui/BaseSpinner.vue';
  import AlertMessage from '@/components/ui/AlertMessage.vue';
  
  const props = defineProps({
    key: {
      type: String,
      required: true
    }
  });
  
  const isLoading = ref(true);
  const isError = ref(false);
  const message = ref('Верифікація вашого email...');
  const authStore = useAuthStore();
  
  onMounted(async () => {
    try {
      await authStore.verifyEmail(props.key);
      message.value = 'Ваш email успішно підтверджено! Тепер ви можете увійти.';
      isError.value = false;
    } catch (error) {
      message.value = 'Помилка верифікації. Можливо, посилання застаріло або недійсне.';
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  });
  </script>