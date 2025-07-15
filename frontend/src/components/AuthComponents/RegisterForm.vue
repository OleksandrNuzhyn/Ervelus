<template>
  <div class="form-container">
    <form
      v-if="!waitingEmailForm"
      @submit.prevent="handleSubmit"
      class="space-y-6"
      novalidate
    >
      <div class="text-center">
        <h2 class="text-3xl font-bold text-white">Join the Ervelus</h2>
        <p class="mt-2 text-gray-300">Create an account</p>
      </div>

      <div>
        <label for="reg-email" class="block text-sm font-semibold text-gray-200">Email</label>
        <input
          id="reg-email"
          type="email"
          v-model="email"
          placeholder="casualtraveller@example.com"
          required
          minlength="5"
          maxlength="254"
          inputmode="email"
          class="w-full px-4 py-2 mt-2 text-gray-200 bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-400"
        />
        <p v-if="errors.email" class="mt-1 text-sm text-red-400">{{ errors.email }}</p>
      </div>

      <div>
        <label for="reg-pass1" class="block text-sm font-semibold text-gray-200">Password</label>
        <div class="relative">
          <input
            id="reg-pass1"
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
        <label for="reg-pass2" class="block text-sm font-semibold text-gray-200">Confirm Password</label>
        <div class="relative">
          <input
            id="reg-pass2"
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

      <p v-if="errors.api" class="text-center text-red-400">{{ errors.api }}</p>

      <div class="space-y-4">
        <div class="flex items-center">
          <input
            id="terms-checkbox"
            type="checkbox"
            v-model="agreedToTerms"
            class="h-4 w-4 rounded border-gray-300 text-sky-500 focus:ring-sky-500"
          />
          <label for="terms-checkbox" class="ml-3 block text-sm text-gray-300">
            I agree to the
            <router-link to="/terms-of-service" target="_blank" class="font-medium text-sky-500 hover:text-sky-300">Terms of Service</router-link>
            and
            <router-link to="/privacy-policy" target="_blank" class="font-medium text-sky-500 hover:text-sky-300">Privacy Policy</router-link>.
          </label>
        </div>
        <p v-if="errors.terms" class="mt-1 text-sm text-red-400">{{ errors.terms }}</p>
      </div>

      <div>
        <button
          type="submit"
          :disabled="isLoading || !agreedToTerms"
          class="w-full py-3 font-bold text-gray-800 transition duration-300 rounded-md disabled:opacity-40 disabled:cursor-not-allowed bg-white/60 backdrop-blur-md border border-white/20 shadow-lg hover:bg-white/20"
        >
          <span v-if="isLoading">Creating…</span>
          <span v-else>Confirm</span>
        </button>
      </div>

      <div class="relative flex items-center py-2">
        <div class="flex-grow border-t border-gray-600"></div>
        <span class="flex-shrink mx-4 text-gray-400">Or</span>
        <div class="flex-grow border-t border-gray-600"></div>
      </div>

      <div>
        <button
          type="button"
          @click="googleLogin"
          :disabled="!isReady || isGoogleLoading || !agreedToTerms"
          class="w-full py-3 font-bold text-white transition duration-300 rounded-md disabled:opacity-45 disabled:cursor-not-allowed bg-sky-500/40 backdrop-blur-md border border-white/20 shadow-lg hover:bg-sky-500/15 flex items-center justify-center gap-2"
        >
          <svg class="w-5 h-5" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M47.532 24.552C47.532 22.92 47.388 21.288 47.076 19.728H24.48V28.944H37.476C36.9 31.932 35.244 34.524 32.844 36.132V42.012H40.728C45.024 38.016 47.532 31.86 47.532 24.552Z" fill="#4285F4"/>
            <path d="M24.48 48.0001C31.068 48.0001 36.636 45.8281 40.728 42.0121L32.844 36.1321C30.588 37.6921 27.756 38.6281 24.48 38.6281C18.156 38.6281 12.792 34.3321 11.016 28.5961H3.012V34.6681C7.032 42.6601 15.192 48.0001 24.48 48.0001Z" fill="#34A853"/>
            <path d="M11.016 28.596C10.536 27.108 10.272 25.548 10.272 23.988C10.272 22.428 10.536 20.868 11.016 19.38L3.012 13.308C1.128 17.1 0 21.396 0 23.988C0 26.58 1.128 30.876 3.012 34.668L11.016 28.596Z" fill="#FBBC05"/>
            <path d="M24.48 9.36C28.116 9.36 31.32 10.608 33.72 12.876L40.944 5.652C36.636 1.956 31.068 0 24.48 0C15.192 0 7.032 5.34 3.012 13.308L11.016 19.38C12.792 13.644 18.156 9.36 24.48 9.36Z" fill="#EA4335"/>
          </svg>
          <span v-if="isGoogleLoading">Please wait...</span>
          <span v-else>Sign up with Google</span>
        </button>
      </div>

      <div class="text-center mt-2">
        <span class="text-sm text-gray-400">Already have an account? </span>
        <router-link to="/login" draggable="false" class="text-sm text-orange-400 hover:text-orange-200">Log in</router-link>
      </div>
    </form>

    <div
      v-else
      class="space-y-6 text-center"
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
        class="w-full py-3 font-bold text-white transition duration-300 rounded-md disabled:opacity-60 disabled:cursor-not-allowed bg-white/10 backdrop-blur-md border border-white/20 shadow-lg hover:bg-white/20"
      >
        <span v-if="isLoading">Sending...</span>
        <span v-else>Resend Confirmation Email</span>
      </button>
       <p v-if="errors.api" class="mt-2 text-sm text-red-400">{{ errors.api }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useTokenClient } from "vue3-google-signin";
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';
import isEmail from 'validator/lib/isEmail';
import eye_of_sauron from '@/assets/geralt_closed.svg';
import eye_of_sauron_looking from '@/assets/geralt_looking.svg';

const email = ref('');
const password1 = ref('');
const password2 = ref('');
const isLoading = ref(false);
const isGoogleLoading = ref(false);
const showPassword1 = ref(false);
const showPassword2 = ref(false);
const agreedToTerms = ref(false);
const errors = ref({
  email: '',
  password1: '',
  password2: '',
  api: '',
  terms: '',
});
const waitingEmailForm = ref(false);
const canResend = ref(false);
let timerId = null;

const router = useRouter();
const authStore = useAuthStore();

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

const { isReady, login: googleLogin } = useTokenClient({
  scope: 'email',
  onSuccess: handleGoogleSuccess,
  onError: handleGoogleError,
});

async function handleGoogleSuccess(response) {
  if (!agreedToTerms.value) {
    errors.value.terms = 'You shall not pass without accepting the terms of service.';
    return;
  }
  isGoogleLoading.value = true;
  errors.value.api = '';
  const accessToken = response.access_token;
  try {
    await api.post('api/auth/google/', { access_token: accessToken });
    await authStore.checkAuth();
    router.push('/dashboard');
  } 
  catch (error) {
    errors.value.api = error.response?.data?.detail || 'Google sign-up failed.';
  } 
  finally {
    isGoogleLoading.value = false;
  }
}

function handleGoogleError() {
  errors.value.api = 'Google sign-up process failed. Please try again.';
}

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
    if (error.response) {
      const { status, data = {} } = error.response;
      switch (status) {
        case 400:
          if (data.email) {
            errors.value.api = Array.isArray(data.email) ? data.email[0] : data.email;
          } 
          else if (data.detail) {
            errors.value.api = data.detail[0];
          } 
          else {
            errors.value.api = 'Invalid request. Please check your email address.';
          }
          break;
        case 500:
          errors.value.api = data.detail || 'Server Error Occured.';
          break;
        default:
          errors.value.api = 'An unexpected error occurred while resending the email.';
      }
    } 
    else {
      errors.value.api = 'Unable to connect to the server. Please check your network connection.';
    }
  } 
  finally {
    isLoading.value = false;
  }
}

function validateForm() {
  errors.value = { email: '', password1: '', password2: '', api: '', terms: '' };
  let isValid = true;

  if (!agreedToTerms.value) {
    errors.value.terms = 'You shall not pass without accepting the terms of service..';
    isValid = false;
  }

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
    errors.value = { email: '', password1: '', password2: '', api: '', terms: '' };

    if (error.response) {
      const { status, data = {} } = error.response;

      switch (status) {
        case 400:
          if (data.email) {
            errors.value.email = Array.isArray(data.email) ? data.email[0] : data.email;
          }
          if (data.password1) {
            errors.value.password1 = Array.isArray(data.password1) ? data.password1[0] : data.password1;
          }
          if (data.password2) {
            errors.value.password2 = Array.isArray(data.password2) ? data.password2[0] : data.password2;
          }
          if (data.non_field_errors) {
            errors.value.api = Array.isArray(data.non_field_errors) ? data.non_field_errors[0] : data.non_field_errors;
          }
          if (!errors.value.email && !errors.value.password1 && !errors.value.password2 && !errors.value.api) {
            errors.value.api = 'Invalid data provided. Please check your input.';
          }
          break;
        
        case 409:
          errors.value.api ='A soul with this name is already wandering the Ervelus.';
          break;

        case 500:
          errors.value.api ='Internal Server Error.';
          break;

        default:
          errors.value.api = `An unexpected error occurred (Status: ${status}). Please try again.`;
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

<style scoped>
.form-container {
  height: 100%;
  width: 67%;
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
  mask-image: radial-gradient(ellipse at center, black 50%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 65%, transparent 100%);
}

.password-toggle-icon {
  opacity: 0.6;
  transition: opacity 0.3s ease-in-out, filter 0.3s ease-in-out;
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
</style>