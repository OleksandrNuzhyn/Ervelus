<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-900 font-serif">
      <form @submit.prevent="handleSubmit" class="w-full max-w-md p-8 space-y-6 bg-gradient-to-b from-purple-965 via-purple-900 to-indigo-900 rounded-xl shadow-2xl text-white" novalidate>
        <div class="text-center">
          <h2 class="text-2xl font-bold mb-2">Set new password</h2>
        </div>
  
        <div>
          <label for="new1" class="block text-sm font-semibold text-gray-300">New password</label>
          <input id="new1" type="password" v-model="password1" placeholder="••••••••" required minlength="8" autocomplete="new-password" class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500" />
          <p v-if="errors.password1" class="mt-1 text-sm text-red-400">{{ errors.password1 }}</p>
        </div>
  
        <div>
          <label for="new2" class="block text-sm font-semibold text-gray-300">Repeat new password</label>
          <input id="new2" type="password" v-model="password2" placeholder="••••••••" required minlength="8" autocomplete="new-password" class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500" />
          <p v-if="errors.password2" class="mt-1 text-sm text-red-400">{{ errors.password2 }}</p>
        </div>
  
        <p v-if="errors.api" class="text-center text-red-400">{{ errors.api }}</p>
  
        <button type="submit" :disabled="isLoading" class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed">
          <span v-if="isLoading">Setting…</span>
          <span v-else>Set password</span>
        </button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import api from '@/services/api';
  
  const route = useRoute();
  const router = useRouter();
  const uid = route.params.uid;
  const token = route.params.token;
  
  const password1 = ref('');
  const password2 = ref('');
  const isLoading = ref(false);
  const errors = ref({ password1: '', password2: '', api: '' });
  
  function validateForm() {
    errors.value = { password1: '', password2: '', api: '' };
    let ok = true;
    if (!password1.value || password1.value.length < 8) {
      errors.value.password1 = 'Your password must contain no fewer than 8 characters.';
      ok = false;
    }
    if (password1.value !== password2.value) {
      errors.value.password2 = 'Passwords are not in harmony.';
      ok = false;
    }
    return ok;
  }
  
  async function handleSubmit() {
    if (!validateForm()) return;
    isLoading.value = true;
    try {
      await api.post('/api/auth/password/reset/confirm/', {
        uid,
        token,
        new_password1: password1.value,
        new_password2: password2.value,
      });
      router.push({ path: '/login', query: { reset: 'done' } }); 
    } 
    catch (error) {
      errors.value = { password1: '', password2: '', api: '' };

      if (error.response) {
        const { status, data = {} } = error.response;

        switch (status) {
          case 400:
            if (data.new_password1) {
              errors.value.password1 = Array.isArray(data.new_password1) ? data.new_password1[0] : data.new_password1;
            }
            if (data.new_password2) {
              errors.value.password2 = Array.isArray(data.new_password2) ? data.new_password2[0] : data.new_password2;
            }
            if (data.token) {
              errors.value.api = Array.isArray(data.token) ? data.token[0] : data.token;
            } 
            else if (data.non_field_errors) {
              errors.value.api = Array.isArray(data.non_field_errors) ? data.non_field_errors[0] : data.non_field_errors;
            } 
            else if (data.detail) {
               errors.value.api = data.detail;
            }
            break;
          case 500:
            errors.value.api = data.detail || 'Server Error Occured.';
            
            break;

          default:
            console.error(`Unexpected error status: ${status}`, error.response);
            errors.value.api = 'An unexpected error occurred.';
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
