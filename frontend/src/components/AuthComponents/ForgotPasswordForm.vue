<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900 font-serif">
    <form @submit.prevent="handleSubmit" 
    class="w-full max-w-md p-8 space-y-6 bg-gradient-to-b from-purple-965 via-purple-900 to-indigo-900 rounded-xl shadow-2xl text-white" 
    novalidate>
      <div class="text-center">
        <h2 class="text-2xl font-bold mb-2">Forgot Password</h2>
        <p class="text-gray-400 text-sm">Enter your email, and we will send you a reset link.</p>
      </div>

      <div>
        <label for="fp-email" class="block text-sm font-semibold text-gray-300">Email</label>
        <input id="fp-email" type="email" v-model="email" placeholder="lostsoul@example.com"
        class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500" 
        required />
        <p v-if="error" class="mt-1 text-sm text-red-400">{{ error }}</p>
      </div>

      <div v-if="sent" class="p-3 rounded bg-green-600 text-sm text-white text-center">
        Link sent! Check your inbox.
      </div>

      <button type="submit" :disabled="isLoading || sent" class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed">
        <span v-if="isLoading">Sending…</span>
        <span v-else>Send reset link</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import isEmail from 'validator/lib/isEmail';

const email = ref('');
const isLoading = ref(false);
const error = ref('');
const sent = ref(false);
const router = useRouter();

watch(email, () => {
  sent.value = false;
  error.value = '';
});

async function handleSubmit() {
  error.value = '';
  if (!isEmail(email.value)) {
    error.value = 'Invalid email format.';
    return;
  }
  isLoading.value = true;
  try {
    await api.post('api/auth/password/reset/', { email: email.value });
    sent.value = true;
  } 
  catch (err) {
    if (err.response) {
      const { status, data = {} } = err.response;
      switch (status) {
        case 500:
          error.value = data.detail || 'A server error occurred.';
          break;
        default:
          error.value = 'An unexpected error occurred.';
      }
    } 
    else {
      error.value = 'Unable to connect to the server. Please check your magic connection.';
    }
  } 
  finally {
    isLoading.value = false;
  }
}
</script>
