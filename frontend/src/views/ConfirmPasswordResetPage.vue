<template>
    <AuthLayout>
      <h2 class="text-3xl font-extrabold text-center text-gray-100">Встановлення нового пароля</h2>
      <form @submit.prevent="handleConfirm" class="mt-8 space-y-6">
        <BaseInput 
          v-model="passwords.new_password1" 
          id="new_password1" 
          type="password" 
          label="Новий пароль"
          :error="serverErrors.new_password1?.join(' ')" 
          required 
        />
        <BaseInput 
          v-model="passwords.new_password2" 
          id="new_password2" 
          type="password" 
          label="Підтвердіть новий пароль"
          :error="serverErrors.new_password2?.join(' ')" 
          required 
        />
        <AlertMessage :message="message" :type="isError ? 'error' : 'success'" />
        <BaseButton :is-loading="isLoading">Змінити пароль</BaseButton>
      </form>
    </AuthLayout>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/auth';
  import AuthLayout from '@/layouts/AuthLayout.vue';
  import BaseInput from '@/components/ui/BaseInput.vue';
  import BaseButton from '@/components/ui/BaseButton.vue';
  import AlertMessage from '@/components/ui/AlertMessage.vue';
  
  const props = defineProps({
    uid: { type: String, required: true },
    token: { type: String, required: true }
  });
  
  const passwords = ref({ new_password1: '', new_password2: '' });
  const isLoading = ref(false);
  const message = ref('');
  const isError = ref(false);
  const serverErrors = ref({});
  const authStore = useAuthStore();
  const router = useRouter();
  
  async function handleConfirm() {
    isLoading.value = true;
    message.value = '';
    isError.value = false;
    serverErrors.value = {};
    
    try {
      await authStore.confirmPasswordReset({ ...passwords.value, ...props });
      message.value = 'Пароль успішно змінено! Перенаправляємо на сторінку входу...';
      setTimeout(() => router.push({ name: 'login' }), 3000);
    } catch (error) {
      if (error.response && error.response.status === 400) {
        serverErrors.value = error.response.data;
        message.value = 'Будь ласка, виправте помилки.'
      } else {
        message.value = 'Помилка. Можливо, посилання недійсне або термін його дії закінчився.';
      }
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }
  </script>