<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900 font-serif">
    <form
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
  </div>
</template>

<script setup>
import { ref } from 'vue';
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

const router = useRouter();

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
    await api.post('/auth/registration/', {
      email: email.value,
      password1: password1.value,
      password2: password2.value,
    });
    router.push({ path: '/login', query: { confirm: 'sent' } });
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
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Alegreya:wght@400;700&display=swap');
.font-alegreya {
    font-family: 'Alegreya', serif;
}

</style>