<template>
  <div class="form-container">
      <form @submit.prevent="handleSubmit" class="space-y-5" novalidate>
        <div class="text-center">
          <h2 class="text-2xl font-bold text-white">Forgot Password</h2>
          <p class="text-gray-400 text-m mt-2">Enter email, and we will grant you mercy</p>
        </div>

        <div>
          <label for="fp-email" class="block text-sm font-semibold text-gray-200 m-0">Email</label>
          <input id="fp-email" type="email" v-model="email" placeholder="lostsoul@example.com"
          class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-400"
          required />
          <p v-if="error" class="mt-1 text-sm text-red-400">{{ error }}</p>
        </div>

        <div v-if="sent" class="-mt-3 text-sm text-green-600 text-left p-1">
          Link sent! Check your inbox.
        </div>

        <button type="submit" :disabled="isLoading || sent" class="w-full py-3 font-bold text-white transition duration-300 rounded-md disabled:opacity-60 disabled:cursor-not-allowed bg-white/10 backdrop-blur-md border border-white/1 shadow-lg hover:bg-white/20">
        <span v-if="isLoading">Sending…</span>
        <span v-else>Send reset link</span>
        </button>
      </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import api from '@/services/api';
import isEmail from 'validator/lib/isEmail';

const email = ref('');
const isLoading = ref(false);
const error = ref('');
const sent = ref(false);

watch(email, () => {
  sent.value = false;
  error.value = '';
});

async function handleSubmit() {
  error.value = '';
  if (!isEmail(email.value)) {
    error.value = 'Invalid email format';
    return;
  }
  isLoading.value = true;
  try {
    await api.post('/api/auth/password/reset/', { email: email.value });
    sent.value = true;
  }
  finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: rgba(10, 10, 10, 0.1) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 2rem;
  font-family: 'Manrope', sans-serif;
  color: #e5e7eb;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
  -webkit-text-fill-color: #e5e7eb !important;
  -webkit-box-shadow: 0 0 0px 1000px #374151 inset !important;
  transition: background-color 5000s ease-in-out 0s;
  font-family: 'Manrope', sans-serif;
}
</style>