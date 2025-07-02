<template>
    <AuthLayout>
      <div>
        <h2 class="text-3xl font-extrabold text-center text-gray-100">Створити новий акаунт</h2>
        <p class="mt-2 text-sm text-center text-gray-400">
          Або
          <RouterLink to="/login" class="font-medium text-purple-400 hover:text-purple-300">
            увійдіть у свій акаунт
          </RouterLink>
        </p>
      </div>
      <form @submit.prevent="handleRegister" class="mt-8 space-y-6">
        <BaseInput
          v-model="formData.email"
          id="email"
          type="email"
          label="Email адреса"
          placeholder="email@example.com"
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
        <BaseInput
          v-model="formData.password2"
          id="password2"
          type="password"
          label="Підтвердіть пароль"
          :error="serverErrors.password2?.join(' ')"
          required
        />
        <AlertMessage :message="serverErrors.non_field_errors?.join(' ')" type="error" />
        <BaseButton :is-loading="isLoading">Зареєструватися</BaseButton>
      </form>
    </AuthLayout>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter, RouterLink } from 'vue-router';
  import { useAuthStore } from '@/stores/auth';
  import AuthLayout from '@/layouts/AuthLayout.vue';
  import BaseInput from '@/components/ui/BaseInput.vue';
  import BaseButton from '@/components/ui/BaseButton.vue';
  import AlertMessage from '@/components/ui/AlertMessage.vue';
  
  const formData = ref({
    email: '',
    password: '',
    password2: ''
  });
  
  const isLoading = ref(false);
  const serverErrors = ref({});
  const authStore = useAuthStore();
  const router = useRouter();
  
  async function handleRegister() {
    isLoading.value = true;
    serverErrors.value = {};
    try {
      await authStore.register(formData.value);
      router.push({ name: 'check-email' });
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
  </script>