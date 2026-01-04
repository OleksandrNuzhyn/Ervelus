<template>
  <div class="form-container">
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-6 text-gray-200" novalidate>
      <div class="text-center">
        <h2 class="medieval text-2xl text-gray-100 mb-1">Set new password</h2>
        <p class="text-gray-300 text-base m-0 leading-relaxed">Enter your new password twice to set it</p>
      </div>
  
      <div class="flex flex-col items-center gap-4 w-full">
        <div class="flex items-center justify-center w-full translate-x-5">
          <div class="relative w-full max-w-[250px]">
            <input id="new1" :type="password1FieldType" v-model="password1" placeholder="New password" required minlength="8" autocomplete="new-password" class="w-full px-0 py-2 text-gray-200 bg-transparent !important border-b border-white/20 focus:border-white/50 focus:outline-none transition-all duration-300 text-center placeholder:text-gray-500 font-light" />
          </div>
          <div class="w-10 ml-2 flex justify-start">
            <img :src="password1Icon" @click="togglePassword1Visibility" draggable="false" class="select-none h-8 w-12 cursor-pointer transition-all duration-300" :class="showPassword1 ? 'opacity-100 glowing-eye' : 'opacity-35'" alt="Toggle password visibility" />
          </div>
        </div>
        <p v-if="errors.password1" class="text-xs text-rose-400 text-center -mt-2">{{ errors.password1 }}</p>

        <div class="flex items-center justify-center w-full translate-x-5">
          <div class="relative w-full max-w-[250px]">
            <input id="new2" :type="password2FieldType" v-model="password2" placeholder="Repeat new password" required minlength="8" autocomplete="new-password" class="w-full px-0 py-2 text-gray-200 bg-transparent !important border-b border-white/20 focus:border-white/50 focus:outline-none transition-all duration-300 text-center placeholder:text-gray-500 font-light" />
          </div>
          <div class="w-10 ml-2 flex justify-start">
            <img :src="password2Icon" @click="togglePassword2Visibility" draggable="false" class="select-none h-8 w-12 cursor-pointer transition-all duration-300" :class="showPassword2 ? 'opacity-100 glowing-eye' : 'opacity-35'" alt="Toggle password visibility" />
          </div>
        </div>
        <p v-if="errors.password2" class="text-xs text-rose-400 text-center -mt-2">{{ errors.password2 }}</p>
      </div>

      <p v-if="errors.api" class="text-sm text-rose-400 text-center">{{ errors.api }}</p>

      <div class="flex justify-center pt-4">
        <button type="submit" :disabled="isLoading" class="manage-button">
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
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 440px;
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
}

@media (max-width: 640px) {
  .form-container {
    padding: 1.5rem;
  }
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
  -webkit-box-shadow: 0 0 0px 1000px rgba(20, 20, 20, 0.95) inset !important;
  transition: background-color 5000s ease-in-out 0s;
}

input[type="password"]::-ms-reveal {
  display: none;
  width: 0;
  height: 0;
}
</style>