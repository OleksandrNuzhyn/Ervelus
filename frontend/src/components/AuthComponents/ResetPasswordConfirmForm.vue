<template>
  <div class="form-container">
    <form @submit.prevent="handleSubmit" class="space-y-6" novalidate>
      <div class="text-center mb-8">
        <h2 class="text-2xl font-bold text-white mb-2">Set new password</h2>
        <p class="text-gray-400 text-sm leading-relaxed">Enter your new password</p>
      </div>
  
      <div class="space-y-4">
        <div>
          <label for="new1" class="block text-sm font-semibold text-gray-200">New Password</label>
          <div class="relative">
            <input 
              id="new1" 
              :type="password1FieldType" 
              v-model="password1" 
              required 
              minlength="8" 
              autocomplete="new-password" 
              class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-400 pr-14" 
            />
            <img :src="password1Icon" @click="togglePassword1Visibility" draggable="false" class="select-none absolute right-1 top-1/2 -translate-y-1/2 mt-1 h-10 w-16 cursor-pointer transition-all duration-300" :class="showPassword1 ? 'opacity-100 glowing-eye' : 'opacity-35'" alt="Toggle password visibility" />
          </div>
          <p v-if="errors.password1" class="mt-1 text-sm text-red-400">{{ errors.password1 }}</p>
        </div>

        <div>
          <label for="new2" class="block text-sm font-semibold text-gray-200">Confirm New Password</label>
          <div class="relative">
            <input 
              id="new2" 
              :type="password2FieldType" 
              v-model="password2" 
              required 
              minlength="8" 
              autocomplete="new-password" 
              class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-400 pr-14" 
            />
            <img :src="password2Icon" @click="togglePassword2Visibility" draggable="false" class="select-none absolute right-1 top-1/2 -translate-y-1/2 mt-1 h-10 w-16 cursor-pointer transition-all duration-300" :class="showPassword2 ? 'opacity-100 glowing-eye' : 'opacity-35'" alt="Toggle password visibility" />
          </div>
          <p v-if="errors.password2" class="mt-1 text-sm text-red-400">{{ errors.password2 }}</p>
        </div>
      </div>

      <p v-if="errors.api" class="text-sm text-red-400 text-center">{{ errors.api }}</p>

      <div class="pt-2">
        <button type="submit" :disabled="isLoading" class="w-full py-3 font-bold text-gray-800 transition duration-300 rounded-md disabled:opacity-40 disabled:cursor-not-allowed bg-gray-400 border border-gray-500 shadow-lg hover:bg-gray-500 hover:text-gray-900">
          <span v-if="isLoading">Setting…</span>
          <span v-else>Set password</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import eye_of_sauron from '@/assets/svg/geralt_closed.svg';
import eye_of_sauron_looking from '@/assets/svg/geralt_looking.svg';

const route = useRoute();
const router = useRouter();
const uid = route.params.uid;
const token = route.params.token;

const password1 = ref('');
const password2 = ref('');
const isLoading = ref(false);
const errors = ref({ password1: '', password2: '', api: '' });

const showPassword1 = ref(false);
const showPassword2 = ref(false);

const password1FieldType = computed(() => showPassword1.value ? 'text' : 'password');
const password1Icon = computed(() => showPassword1.value ? eye_of_sauron_looking : eye_of_sauron);

const password2FieldType = computed(() => showPassword2.value ? 'text' : 'password');
const password2Icon = computed(() => showPassword2.value ? eye_of_sauron_looking : eye_of_sauron);

function togglePassword1Visibility() {
  showPassword1.value = !showPassword1.value;
}

function togglePassword2Visibility() {
  showPassword2.value = !showPassword2.value;
}

function validateForm() {
  errors.value = { password1: '', password2: '', api: '' };
  let ok = true;

  if (!password1.value) {
    errors.value.password1 = 'Password is required';
    ok = false;
  } 
  else if (password1.value.length < 8) {
    errors.value.password1 = 'Minimum 8 characters required';
    ok = false;
  }

  if (!password2.value) {
    errors.value.password2 = 'Please confirm password';
    ok = false;
  } 
  else if (password1.value !== password2.value) {
    errors.value.password2 = 'Passwords are not in harmony';
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

      if (status === 400) {
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
      }
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

.glowing-eye {
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.6)) drop-shadow(0 0 12px rgba(77, 188, 255, 0.5));
  animation: shake-subtle 1.7s ease-in-out infinite;
}

@keyframes shake-subtle {
  0%, 100% { transform: translate(0, 0); }
  20% { transform: translate(-1.3px, -1.3px); }
  40% { transform: translate(1.7px, 0.8px); }
  60% { transform: translate(-1px, 1.5px); }
  80% { transform: translate(1.7px, -1.3px); }
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

input[type="password"]::-ms-reveal {
  display: none;
  width: 0;
  height: 0;
}
</style>