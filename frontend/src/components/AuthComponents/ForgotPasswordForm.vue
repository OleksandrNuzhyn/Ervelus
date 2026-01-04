<template>
  <div class="form-container">
      <form @submit.prevent="handleSubmit" class="flex flex-col gap-6 text-gray-200" novalidate>
        <div class="text-center">
          <h2 class="medieval text-2xl text-gray-100 mb-1">{{ sent ? 'Success' : 'Forgot Password' }}</h2>
          <p class="text-gray-300 text-base m-0 leading-relaxed">
            {{ sent ? 'Link sent! Check your inbox' : 'Enter email, and we will grant you mercy' }}
          </p>
        </div>

        <div v-if="!sent" class="flex flex-col items-center">
          <input id="fp-email" type="email" v-model="email" placeholder="lostsoul@example.com"
          class="w-full max-w-[280px] px-0 py-2 text-gray-200 bg-transparent !important border-b border-white/20 focus:border-white/50 focus:outline-none transition-all duration-300 text-center placeholder:text-gray-500 font-light"
          required />
          <p v-if="error" class="mt-2 text-sm text-rose-400 text-center">{{ error }}</p>
        </div>

        <div class="flex justify-center pt-4">
          <button v-if="!sent" type="submit" :disabled="isLoading" class="manage-button">
            <span v-if="isLoading">Sending…</span>
            <span v-else>Send reset link</span>
          </button>
          <router-link v-else to="/login" class="manage-button">Back to Entrance</router-link>
        </div>
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
  catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      error.value = error.response.data.detail;
    } else {
      error.value = 'An error occurred. Please try again';
    }
  }
  finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');

.medieval {
  font-family: 'MedievalSharp', cursive;
}

.form-container {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
}

.manage-button {
  display: inline-block;
  width: auto;
  min-width: 250px;
  text-align: center;
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: 9999px;
  padding: 0.9rem 2.25rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #9ca3af;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  cursor: pointer;
}

.manage-button:not(:disabled):hover {
  background: rgba(129, 180, 253, 0.1);
  color: #81b4fd;
  border-color: rgba(129, 180, 253, 0.4);
}

.manage-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
  -webkit-text-fill-color: #e5e7eb !important;
  -webkit-box-shadow: 0 0 0px 1000px rgba(20, 20, 20, 0.95) inset !important;
  transition: background-color 5000s ease-in-out 0s;
}
</style>