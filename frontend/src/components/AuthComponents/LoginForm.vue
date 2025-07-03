<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-900 font-serif">
      
      <form 
        @submit.prevent="handleSubmit" 
        class="w-full max-w-md p-8 space-y-6 bg-gray-800 border border-gray-700 rounded-xl shadow-2xl"
      >
        <div class="text-center">
          <h2 class="text-3xl font-bold text-red-500">Вхід до Цитаделі</h2>
          <p class="mt-2 text-gray-400">Введіть ваші дані, щоб продовжити</p>
        </div>
  
        <div>
          <label for="email" class="block text-sm font-semibold text-gray-400">Електронна пошта</label>
          <input 
            id="email"
            type="email"
            v-model="email"
            placeholder="stranger@example.com"
            class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-400">{{ errors.email }}</p>
        </div>
  
        <div>
          <label for="password" class="block text-sm font-semibold text-gray-400">Секретне слово</label>
          <input 
            id="password"
            type="password"
            v-model="password"
            placeholder="••••••••"
            class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
          />
          <p v-if="errors.password" class="mt-1 text-sm text-red-400">{{ errors.password }}</p>
        </div>
  
        <p v-if="errors.api" class="text-center text-red-400">{{ errors.api }}</p>
  
        <div>
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 font-bold text-white transition duration-300 bg-red-700 rounded-md hover:bg-red-800 disabled:bg-red-900 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading">Перевірка...</span>
            <span v-else>Увійти</span>
          </button>
        </div>
  
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import { useRouter } from 'vue-router';
  import api from '@/services/api';
  
  const email = ref('');
  const password = ref('');
  const isLoading = ref(false);
  const errors = ref({
    email: '',
    password: '',
    api: ''
  });
  
  const authStore = useAuthStore();
  const router = useRouter();
  
  function validateForm() {
    errors.value = { email: '', password: '', api: '' };
  
    let isValid = true;
    //типи валідації емейлу validator.js (isEmail(str)
    if (!email.value) {
      errors.value.email = 'Поле пошти не може бути порожнім.';
      isValid = false;
    }
    
    if (!password.value) {
      errors.value.password = 'Будь ласка, введіть ваше секретне слово.';
      isValid = false;
    }
  
    return isValid;
  }
  
  async function handleSubmit() {
    if (!validateForm()) {
      return;
    }
    
    isLoading.value = true;
  
    try {
      await api.post('/auth/login/', {
        email: email.value,
        password: password.value,
      });

      await authStore.checkAuth();

      router.push('/dashboard');

    } catch (error) {
        //брати конкретний еррор і виводити його
      if (error.response && error.response.status >= 400) {
        errors.value.api = 'Невірне ім\'я або секретне слово. Спробуйте ще раз.';
      }
       else {
        errors.value.api = 'Не вдалося з\'єднатися з сервером. Перевірте з\'єднання.';
      }
    }
     finally {
      isLoading.value = false;
    }
  }

  </script>
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
  .font-serif {
    font-family: 'Cinzel', serif;
  }
  </style>