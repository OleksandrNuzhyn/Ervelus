<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-900 font-serif">
      
      <form 
        @submit.prevent="handleSubmit" 
        class="w-full max-w-md p-8 space-y-6 bg-gradient-to-b from-purple-965 via-purple-900 to-indigo-900 rounded-xl shadow-2xl text-gray-300"
      >
        <div v-if="showConfirmBanner" class="mb-4 p-3 rounded bg-green-600 text-white text-sm">
          We have sent a confirmation email. Please check your email.
        </div>
        <p v-if="resetSent" class="mb-4 p-3 rounded bg-green-600 text-white text-sm">Reset link has been sent. Check your e-mail.</p>
        <p v-if="resetDone" class="mb-4 p-3 rounded bg-green-600 text-white text-sm">Password changed successfully. You shall pass.</p>

        <div class="text-center">
          <h2 class="text-3xl font-bold text white">Entrance to the Ervelus</h2>
          <p class="mt-2 text-gray-400">Inscribe your name to proceed</p>
        </div>
  
        <div>
          <label for="email" class="block text-sm font-semibold text-gray-400">Email</label>
          <input 
            id="email"
            type="email"
            v-model="email"
            placeholder="casualtraveller@example.com"
            required
            minlength="5"
            maxlength="254"
            inputmode="email"
            class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-400">{{ errors.email }}</p>
        </div>
  
        <div>
          <label for="password" class="block text-sm font-semibold text-gray-400">Password</label>
          <input 
            id="password"
            type="password"
            v-model="password"
            placeholder="••••••••"
            required
            minlength="8"
            autocomplete="current-password"
            class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
          />
          <p v-if="errors.password" class="mt-1 text-sm text-red-400">{{ errors.password }}</p>
        </div>
  
        <p v-if="errors.api" class="text-center text-red-400">{{ errors.api }}</p>
  
        <div>
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading">Uncovering the truth...</span>
            <span v-else>Log in</span>
          </button>
        </div>
  
        <div class="text-right">
          <router-link to="/forgot-password" class="text-xs text-gray-400 hover:text-gray-200">Lost the keyword?</router-link>
        </div>
  
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import isEmail from 'validator/lib/isEmail';
  import { useAuthStore } from '@/stores/auth';
  import { useRouter, useRoute } from 'vue-router';
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
  const route = useRoute();

  const showConfirmBanner = computed(() => route.query.confirm === 'sent');
  const resetSent = computed(() => route.query.reset === 'sent');
  const resetDone = computed(() => route.query.reset === 'done');
  
  function validateForm() {
    errors.value = { email: '', password: '', api: '' };
  
    let isValid = true;
    if (!email.value) {
      errors.value.email = 'The email field cannot be empty.';
      isValid = false;
    } 
    else if (!isEmail(email.value)) {
      errors.value.email = 'Incorrect email format.';
      isValid = false;
    }
    
    if (!password.value) {
      errors.value.password = 'Please enter your password.';
      isValid = false;
    } 
    else if (password.value.length < 8) {
      errors.value.password = 'Your password must contain no fewer than 8 characters.';
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
      await api.post('api/auth/login/', {
        email: email.value,
        password: password.value,
      });

      await authStore.checkAuth();

      router.push('/dashboard');

    } 
    catch (error) {
      if (error.response) {
        const { status, data = {} } = error.response;

        if (data.email) {
          errors.value.email = Array.isArray(data.email) ? data.email[0] : data.email;
        }
        if (data.password) {
          errors.value.password = Array.isArray(data.password) ? data.password[0] : data.password;
        }
        if (data.detail) {
          errors.value.api = data.detail;
        } 
        else if (Array.isArray(data.non_field_errors)) {
          errors.value.api = data.non_field_errors[0];
        } 
        else {
          switch (status) {
            case 400:
              errors.value.api = 'Incorrect email or password.';
              break;
            case 401:
              errors.value.api = 'Not authorized. Check your credentials.';
              break;
            case 403:
              errors.value.api = 'Access denied. Not enough access rights.';
              break;
            case 404:
              errors.value.api = 'What you seek is lost';
              break;
            case 500:
              errors.value.api = 'Internal server error. Seek again later.';
              break;
            default:
              errors.value.api = 'An error occurred. Try once more';
          }
        }
      } 
      else {
        errors.value.api = 'Unable to connect to the server. Please check your magic connection.';
      }
    }
     finally {
      isLoading.value = false;
    }
  }

  </script>

  <style scoped>

  @import url('https://fonts.googleapis.com/css2?family=Alegreya:wght@400;700&display=swap');
  .font-alegreya {
    font-family: 'Alegreya', serif;
  }
  
  </style>