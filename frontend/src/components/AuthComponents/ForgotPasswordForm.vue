<template>
  <div class="form-container">
      <form @submit.prevent="handleSubmit" class="space-y-6" novalidate>
        <div class="text-center mb-8">
          <h2 class="text-2xl font-bold text-white mb-2">{{ sent ? $t('auth.success') : $t('auth.forgot_password_title') }}</h2>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ sent ? $t('auth.link_sent') : $t('auth.enter_email_reset') }}
          </p>
        </div>

        <div v-if="!sent">
          <label for="fp-email" class="block text-sm font-semibold text-gray-200">{{ $t('auth.email_label') }}</label>
          <input 
            id="fp-email" 
            type="email" 
            v-model="email" 
            class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-400"
            required 
          />
          <p v-if="error" class="mt-2 text-sm text-red-400">{{ error }}</p>
        </div>

        <div class="pt-2">
          <button v-if="!sent" type="submit" :disabled="isLoading" class="w-full py-3 font-bold text-gray-800 transition duration-300 rounded-md disabled:opacity-40 disabled:cursor-not-allowed bg-gray-400 border border-gray-500 shadow-lg hover:bg-gray-500 hover:text-gray-900">
            <span v-if="isLoading">{{ $t('auth.sending') }}</span>
            <span v-else>{{ $t('auth.send_reset_link') }}</span>
          </button>
          <router-link v-else to="/login" class="w-full py-3 inline-block text-center font-bold text-gray-800 transition duration-300 rounded-md bg-gray-400 border border-gray-500 shadow-lg hover:bg-gray-500 hover:text-gray-900">{{ $t('auth.back_to_login') }}</router-link>
        </div>

        <div v-if="!sent" class="text-center">
          <router-link to="/login" class="text-sm text-sky-200 hover:text-sky-100">{{ $t('auth.back_to_login') }}</router-link>
        </div>
      </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '@/services/api';
import isEmail from 'validator/lib/isEmail';

const { t } = useI18n();
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
    error.value = t('auth.error_email_format');
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
      error.value = t('auth.error_generic');
    }
  }
  finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.form-container {
  height: 100%;
  margin-left: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: rgba(10, 10, 10, 0.3) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 2rem;
  font-family: 'Manrope', sans-serif;
  color: #e5e7eb;
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