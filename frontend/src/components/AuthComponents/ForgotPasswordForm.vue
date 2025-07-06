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

      <div v-if="sent && canResend" class="p-3 rounded bg-blue-600 text-sm text-white text-center">
        Didn't get the email? You can send it again.
      </div>

      <button type="submit" :disabled="isLoading || (sent && !canResend)" class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed">
        <span v-if="isLoading">Sending…</span>
        <span v-else>Send reset link</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import isEmail from 'validator/lib/isEmail';

const email = ref('');
const isLoading = ref(false);
const error = ref('');
const sent = ref(false);
const canResend = ref(false);
let timerId;
const router = useRouter();

async function handleSubmit() {
  error.value = '';
  if (!isEmail(email.value)) {
    error.value = 'Invalid email format.';
    return;
  }
  isLoading.value = true;
  try {
    await api.post('/auth/password/reset/', { email: email.value });
    sent.value = true;
    canResend.value = false;
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      canResend.value = true;
    }, 30000);
  } catch (err) {
    error.value = 'Something went wrong.';
  } finally {
    isLoading.value = false;
  }
}

import { onUnmounted } from 'vue';
onUnmounted(() => clearTimeout(timerId));
</script>

<style scoped></style> 