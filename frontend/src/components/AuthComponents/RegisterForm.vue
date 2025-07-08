<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900 font-serif">
    <form
      v-if="!waitingEmailForm"
      @submit.prevent="handleSubmit"
      class="w-full max-w-md p-8 space-y-6 bg-gradient-to-b from-purple-965 via-purple-950 to-indigo-980 rounded-xl shadow-2xl text-gray-300"
      novalidate
    >
      <div class="text-center">
        <h2 class="text-3xl font-bold text-white">Join the Ervelus</h2>
        <p class="mt-2 text-gray-400">Create an account</p>
      </div>

      <div>
        <label for="reg-email" class="block text-sm font-semibold text-gray-400">Email</label>
        <input
          id="reg-email"
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
        <label for="reg-pass1" class="block text-sm font-semibold text-gray-400">Password</label>
        <input
          id="reg-pass1"
          type="password"
          v-model="password1"
          placeholder="••••••••"
          required
          minlength="8"
          autocomplete="new-password"
          class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
        />
        <p v-if="errors.password1" class="mt-1 text-sm text-red-400">{{ errors.password1 }}</p>
      </div>

      <div>
        <label for="reg-pass2" class="block text-sm font-semibold text-gray-400">Confirm Password</label>
        <input
          id="reg-pass2"
          type="password"
          v-model="password2"
          placeholder="••••••••"
          required
          minlength="8"
          autocomplete="new-password"
          class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
        />
        <p v-if="errors.password2" class="mt-1 text-sm text-red-400">{{ errors.password2 }}</p>
      </div>

      <p v-if="errors.api" class="text-center text-red-400">{{ errors.api }}</p>

      <div>
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading">Creating…</span>
          <span v-else>Confirm</span>
        </button>
      </div>
    </form>

    <div
      v-else
      class="w-full max-w-md p-8 space-y-6 bg-gradient-to-b from-purple-965 via-purple-950 to-indigo-980 rounded-xl shadow-2xl text-white text-center"
    >
      <h2 class="text-2xl font-bold">Confirm your Email</h2>
      <p class="text-gray-400">
        We've sent a confirmation link to <strong>{{ email }}</strong>. Please check your inbox and spam folder.
      </p>
      
      <p v-if="canResend" class="text-green-400 text-sm">
        Didn't get the email? You can try sending it again.
      </p>

      <button
        @click="handleResendEmail"
        :disabled="!canResend || isLoading"
        class="w-full py-3 font-bold text-white transition duration-300 bg-gradient-to-r from-orange-500 to-orange-700 rounded-md hover:from-orange-600 hover:to-orange-800 disabled:opacity-60 disabled:cursor-not-allowed"
      >
        <span v-if="isLoading">Sending...</span>
        <span v-else>Resend Confirmation Email</span>
      </button>
       <p v-if="errors.api" class="mt-2 text-sm text-red-400">{{ errors.api }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import isEmail from 'validator/lib/isEmail';

const email = ref('');
const password1 = ref('');
const password2 = ref('');
const isLoading = ref(false);
const errors = ref({
  email: '',
  password1: '',
  password2: '',
  api: '',
});
const waitingEmailForm = ref(false);
const canResend = ref(false);
let timerId = null;

const router = useRouter();

function startResendTimer() {
  canResend.value = false;
  
  if (timerId) {
    clearTimeout(timerId);
  }

  timerId = setTimeout(() => {
    canResend.value = true;
    timerId = null;
  }, 240000);
}

async function handleResendEmail() {
  if (!canResend.value) return;
  isLoading.value = true;
  errors.value.api = '';
  try {
    await api.post('api/auth/registration/resend-email/', { email: email.value });
    startResendTimer();
  } 
  catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      errors.value.api = error.response.data.detail;
    } 
    else {
      errors.value.api = 'An error occurred while resending the email.';
    }
  } 
  finally {
    isLoading.value = false;
  }
}

function validateForm() {
  errors.value = { email: '', password1: '', password2: '', api: '' };
  let isValid = true;

  if (!email.value) {
    errors.value.email = 'Email is required.';
    isValid = false;
  } 
  else if (!isEmail(email.value)) {
    errors.value.email = 'Invalid email format.';
    isValid = false;
  }

  if (!password1.value) {
    errors.value.password1 = 'Password is required.';
    isValid = false;
  } 
  else if (password1.value.length < 8) {
    errors.value.password1 = 'Your password must contain no fewer than 8 characters.';
    isValid = false;
  }

  if (!password2.value) {
    errors.value.password2 = 'Please confirm password.';
    isValid = false;
  } 
  else if (password1.value !== password2.value) {
    errors.value.password2 = 'Passwords are not in harmony.';
    isValid = false;
  }

  return isValid;
}

async function handleSubmit() {
  if (!validateForm()) return;
  isLoading.value = true;
  try {
    await api.post('api/auth/registration/', {
      email: email.value,
      password1: password1.value,
      password2: password2.value,
    });
    waitingEmailForm.value = true;
    startResendTimer();
  }
  catch (error) {
    if (error.response) {
      const { status, data = {} } = error.response;

      if (data.email) errors.value.email = Array.isArray(data.email) ? data.email[0] : data.email;
      if (data.password1) errors.value.password1 = Array.isArray(data.password1) ? data.password1[0] : data.password1;
      if (data.non_field_errors) errors.value.api = data.non_field_errors[0];
      else if (data.detail) errors.value.api = data.detail;
      else {
        switch (status) {
          case 400:
            errors.value.api = 'Invalid data. Please check fields.';
            break;
          case 409:
            errors.value.api = 'A soul with that name is already wandering the Ervelus.';
            break;
          case 500:
            errors.value.api = 'Internal Server Error. Please try again later.';
            break;
          default:
            errors.value.api = 'Error ' + status + '. Try once more.';
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

onUnmounted(() => {
  if (timerId) {
    clearTimeout(timerId);
  }
});

</script>