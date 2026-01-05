<template>
    <div class="form-container">
      <form 
        @submit.prevent="handleSubmit" 
        class="space-y-6"
        novalidate
      >
        <div class="text-center mb-2">
          <router-link to="/" class="inline-block text-gray-100 hover:text-gray-300 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-8 w-8">
              <path d="M11.47 3.84a.75.75 0 011.06 0l8.69 8.69a.75.75 0 101.06-1.06l-8.689-8.69a2.25 2.25 0 00-3.182 0l-8.69 8.69a.75.75 0 001.061 1.06l8.69-8.69z" />
              <path d="M12 5.432l8.159 8.159c.03.03.06.058.091.086v6.198c0 1.035-.84 1.875-1.875 1.875H15a.75.75 0 01-.75-.75v-4.5a.75.75 0 00-.75-.75h-3a.75.75 0 00-.75.75V21a.75.75 0 01-.75.75H5.625a1.875 1.875 0 01-1.875-1.875v-6.198a2.29 2.29 0 00.091-.086L12 5.43z" />
            </svg>
          </router-link>
        </div>

        <div class="text-center mb-10">
          <h2 class="text-3xl font-bold text-white">Entrance to the Ervelus</h2>
        </div>

        <div>
          <button
            type="button"
            @click="login"
            :disabled="!isReady || isGoogleLoading"
            class="w-full py-3 font-bold text-gray-800 transition duration-300 rounded-md disabled:opacity-45 disabled:cursor-not-allowed bg-gray-300 border border-gray-400 shadow-lg hover:bg-gray-400 flex items-center justify-center gap-2"
          >
            <svg class="w-5 h-5" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M47.532 24.552C47.532 22.92 47.388 21.288 47.076 19.728H24.48V28.944H37.476C36.9 31.932 35.244 34.524 32.844 36.132V42.012H40.728C45.024 38.016 47.532 31.86 47.532 24.552Z" fill="#4285F4"/>
              <path d="M24.48 48.0001C31.068 48.0001 36.636 45.8281 40.728 42.0121L32.844 36.1321C30.588 37.6921 27.756 38.6281 24.48 38.6281C18.156 38.6281 12.792 34.3321 11.016 28.5961H3.012V34.6681C7.032 42.6601 15.192 48.0001 24.48 48.0001Z" fill="#34A853"/>
              <path d="M11.016 28.596C10.536 27.108 10.272 25.548 10.272 23.988C10.272 22.428 10.536 20.868 11.016 19.38L3.012 13.308C1.128 17.1 0 21.396 0 23.988C0 26.58 1.128 30.876 3.012 34.668L11.016 28.596Z" fill="#FBBC05"/>
              <path d="M24.48 9.36C28.116 9.36 31.32 10.608 33.72 12.876L40.944 5.652C36.636 1.956 31.068 0 24.48 0C15.192 0 7.032 5.34 3.012 13.308L11.016 19.38C12.792 13.644 18.156 9.36 24.48 9.36Z" fill="#EA4335"/>
            </svg>
            <span v-if="isGoogleLoading">Please wait...</span>
            <span v-else>Sign in with Google</span>
          </button>
          <p class="text-sm text-center text-gray-400 mt-4 mb-2">
            By continuing, you agree to our
            <router-link to="/terms-of-service" target="_blank" class="text-sky-200 hover:text-sky-100 hover:underline">Terms</router-link> & <router-link to="/privacy-policy" target="_blank" class="text-sky-200 hover:text-sky-100 hover:underline">Privacy</router-link>
          </p>
        </div>

        <div class="relative flex items-center py-2 mt-4 mb-2">
            <div class="flex-grow border-t border-gray-600"></div>
            <span class="flex-shrink mx-4 text-gray-400">Or continue with</span>
            <div class="flex-grow border-t border-gray-600"></div>
        </div>
  
        <div>
          <label for="email" class="block text-sm font-semibold text-gray-200">Email</label>
          <input 
            id="email"
            type="email"
            v-model="email"
            required
            minlength="5"
            maxlength="254"
            inputmode="email"
            class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-400">{{ errors.email }}</p>
        </div>
  
        <div>
          <label for="password" class="block text-sm font-semibold text-gray-200">Password</label>
          <div class="relative">
            <input 
              id="password"
              :type="passwordFieldType"
              v-model="password"
              required
              minlength="8"
              autocomplete="current-password"
              class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500 pr-12"
            />
            <img :src="passwordIcon" @click="togglePasswordVisibility" draggable="false" class="select-none absolute right-1 top-1/2 -translate-y-1/2 mt-1 h-10 w-16 cursor-pointer transition-all duration-300" :class="showPassword ? 'opacity-100 glowing-eye' : 'opacity-35'" alt="Toggle password visibility" />
          </div>
          <p v-if="errors.password" class="mt-1 text-sm text-red-400">{{ errors.password }}</p>
        </div>
  
        <p v-if="errors.api" class="text-center text-red-400">{{ errors.api }}</p>

        <div class="mt-8">
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 font-bold text-gray-800 transition duration-300 rounded-md disabled:opacity-60 disabled:cursor-not-allowed bg-gray-400 border border-gray-500 shadow-lg hover:bg-gray-500 hover:text-gray-900"
          >
            <span v-if="isLoading">Uncovering the truth...</span>
            <span v-else>Sign In</span>
          </button>
        </div>
        
        <div class="space-y-4 mt-3">
          <div class="text-right">
            <router-link to="/forgot-password" draggable="false" class="text-sm text-gray-400 hover:text-gray-200">Lost the keyword?</router-link>
          </div>
          <div class="text-center">
            <span class="text-sm text-gray-400">Don't have an account? </span>
            <router-link to="/register" draggable="false" class="text-sm text-sky-200 hover:text-sky-100">Register here</router-link>
          </div>
        </div>
      </form>
    </div>
</template>
  
<script setup>
import { ref, computed } from 'vue';
import { useTokenClient } from "vue3-google-signin";
import isEmail from 'validator/lib/isEmail';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import eye_of_sauron from '@/assets/svg/geralt_closed.svg';
import eye_of_sauron_looking from '@/assets/svg/geralt_looking.svg';

const email = ref('');
const password = ref('');
const isLoading = ref(false);
const isGoogleLoading = ref(false);
const showPassword = ref(false);
const errors = ref({
  email: '',
  password: '',
  api: ''
});

const passwordFieldType = computed(() => showPassword.value ? 'text' : 'password');
const passwordIcon = computed(() => showPassword.value ? eye_of_sauron_looking : eye_of_sauron);

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

const authStore = useAuthStore();
const router = useRouter();

const { isReady, login } = useTokenClient({
  scope: 'email',
  onSuccess: handleLoginSuccess,
  onError: handleLoginError,
});

async function handleLoginSuccess(response) {
  isGoogleLoading.value = true;
  errors.value.api = '';
  const accessToken = response.access_token;
  try {
    const response = await api.post('/api/auth/google/', { access_token: accessToken });
    const token = response.data.key;
    if (token) {
      localStorage.setItem('user-token', token);

      if (response.data.is_registration) {
        window.gtag('event', 'user_sign_up');
      }

      await authStore.checkAuth();
      router.push('/dashboard');
    }
  } 
  catch (error) {
    if (error.response) {
      errors.value.api = error.response?.data?.detail || 'Google sign-in failed';
    }
  } 
  finally {
    isGoogleLoading.value = false;
  }
}

function handleLoginError() {
  errors.value.api = 'Google sign-in failed';
}

function validateForm() {
  errors.value = { email: '', password: '', api: '' };

  let isValid = true;
  if (!email.value) {
    errors.value.email = 'The email field cannot be empty';
    isValid = false;
  } 
  else if (!isEmail(email.value)) {
    errors.value.email = 'Incorrect email format';
    isValid = false;
  }
  
  if (!password.value) {
    errors.value.password = 'Please enter your password';
    isValid = false;
  } 
  else if (password.value.length < 8) {
    errors.value.password = 'Your password must contain no fewer than 8 characters';
    isValid = false;
  }

  return isValid;
}

async function handleSubmit() {
  if (!validateForm()) {
    return;
  }
  
  isLoading.value = true;

  try {
    const response = await api.post('/api/auth/login/', {
      email: email.value,
      password: password.value,
    });
    const token = response.data.key;
    if (token) {
      localStorage.setItem('user-token', token);
      await authStore.checkAuth();
      router.push('/dashboard');
    }
  }
  catch (error) {
    errors.value = { email: '', password: '', api: '' };
    if (error.response) {
      if (error.response.status === 400) {
        const { data = {} } = error.response;
        if (data.non_field_errors && data.non_field_errors.length > 0) {
          errors.value.api = data.non_field_errors[0];
        } 
        else {
          errors.value.api = 'Incorrect email or password. Please try again';
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