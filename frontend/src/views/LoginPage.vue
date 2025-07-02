<template>
    <AuthLayout>
      <div>
        <h2 class="text-3xl font-extrabold text-center text-gray-100">Вхід в акаунт</h2>
        <p class="mt-2 text-sm text-center text-gray-400">
          Або
          <RouterLink to="/register" class="font-medium text-purple-400 hover:text-purple-300">
            створіть новий акаунт
          </RouterLink>
        </p>
      </div>
  
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <BaseInput
          v-model="formData.email"
          id="email"
          type="email"
          label="Email адреса"
          :error="serverErrors.email?.join(' ')"
          required
        />
        <BaseInput
          v-model="formData.password"
          id="password"
          type="password"
          label="Пароль"
          :error="serverErrors.password?.join(' ')"
          required
        />
  
        <div class="flex items-center justify-end">
          <div class="text-sm">
            <RouterLink to="/password-reset" class="font-medium text-purple-400 hover:text-purple-300">
              Забули пароль?
            </RouterLink>
          </div>
        </div>
        
        <AlertMessage :message="serverErrors.non_field_errors?.join(' ')" type="error" />
  
        <BaseButton :is-loading="isLoading">Увійти</BaseButton>
      </form>
      
      <div class="mt-6">
        <div class="relative">
          <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-gray-600" /></div>
          <div class="relative flex justify-center text-sm"><span class="px-2 text-gray-400 bg-gray-800">Або увійдіть через</span></div>
        </div>
        <div id="google-signin-button" class="flex justify-center mt-6"></div>
      </div>
    </AuthLayout>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import { RouterLink } from 'vue-router';
  import AuthLayout from '@/layouts/AuthLayout.vue';
  import BaseInput from '@/components/ui/BaseInput.vue';
  import BaseButton from '@/components/ui/BaseButton.vue';
  import AlertMessage from '@/components/ui/AlertMessage.vue';
  
  const formData = ref({ email: '', password: '' });
  const isLoading = ref(false);
  const serverErrors = ref({});
  const authStore = useAuthStore();
  
  async function handleLogin() {
    isLoading.value = true;
    serverErrors.value = {};
    try {
      await authStore.login(formData.value);
      // Редірект відбувається всередині Pinia action
    } catch (error) {
      if (error.response && error.response.status === 400) {
        serverErrors.value = error.response.data;
      } else {
        serverErrors.value = { non_field_errors: ['Не вдалося підключитися до сервера.'] };
      }
    } finally {
      isLoading.value = false;
    }
  }
  
  // Код для Google Sign-In
  onMounted(() => {
    if (window.google) {
      window.google.accounts.id.initialize({
        client_id: 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com', // <-- ЗАМІНІТЬ НА ВАШ ID
        callback: handleGoogleCallback,
      });
      window.google.accounts.id.renderButton(
        document.getElementById('google-signin-button'),
        { theme: 'outline', size: 'large', type: 'standard' }
      );
    }
  });
  
  async function handleGoogleCallback(response) {
    isLoading.value = true;
    serverErrors.value = {};
    try {
      // Припускаємо, що dj-rest-auth налаштований на прийом ID токена (credential)
      // як access_token. Це поширена конфігурація.
      await authStore.handleGoogleLogin(response.credential);
    } catch (error) {
      serverErrors.value = { non_field_errors: ["Помилка входу через Google."] };
    } finally {
      isLoading.value = false;
    }
  }
  </script>