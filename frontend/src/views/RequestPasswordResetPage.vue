<template>
    <AuthLayout>
      <h2 class="text-3xl font-extrabold text-center text-gray-100">Відновлення пароля</h2>
      <p class="mt-2 text-sm text-center text-gray-400">
        Введіть ваш email, і ми надішлемо вам посилання для встановлення нового пароля.
      </p>
      <form @submit.prevent="handleResetRequest" class="mt-8 space-y-6">
        <BaseInput v-model="email" id="email" type="email" label="Email адреса" required />
        <AlertMessage :message="message" :type="isError ? 'error' : 'success'" />
        <BaseButton :is-loading="isLoading">Надіслати посилання</BaseButton>
      </form>
       <div class="mt-4 text-sm text-center">
          <RouterLink to="/login" class="font-medium text-purple-400 hover:text-purple-300">
            Повернутися до входу
          </RouterLink>
        </div>
    </AuthLayout>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import { RouterLink } from 'vue-router';
  import AuthLayout from '@/layouts/AuthLayout.vue';
  import BaseInput from '@/components/ui/BaseInput.vue';
  import BaseButton from '@/components/ui/BaseButton.vue';
  import AlertMessage from '@/components/ui/AlertMessage.vue';
  
  const email = ref('');
  const isLoading = ref(false);
  const message = ref('');
  const isError = ref(false);
  const authStore = useAuthStore();
  
  async function handleResetRequest() {
    isLoading.value = true;
    message.value = '';
    isError.value = false;
    try {
      await authStore.requestPasswordReset(email.value);
      message.value = 'Якщо цей email зареєстрований, на нього буде надіслано лист для відновлення.';
    } catch (error) {
      message.value = 'Сталася помилка. Спробуйте ще раз.';
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }
  </script>