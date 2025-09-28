<template>
  <div class="w-full max-w-xl mx-auto px-4 md:px-8 pt-5 pb-16">
    <div class="bg-black/30 backdrop-blur-sm rounded-lg border border-white/10 p-6">
      <h1 class="text-3xl font-bold medieval text-center">Contact Us</h1>
      <p class="mt-2 text-sm text-gray-400 text-center">Leave your email and ideas/suggestions here.</p>

      <form class="mt-6 space-y-4" @submit.prevent="onSubmit">
        <div>
          <label for="contact-email" class="block text-sm text-gray-300 mb-1">Email</label>
          <input
            id="contact-email"
            type="email"
            v-model.trim="email"
            class="w-full rounded-md bg-gray-800 border border-gray-700 focus:border-gray-500 focus:outline-none px-3 py-2 text-gray-100 placeholder-gray-500"
            placeholder="you@example.com"
            :disabled="submitting"
            required
          />
          <p v-if="emailError" class="mt-1 text-xs text-red-400">{{ emailError }}</p>
        </div>

        <div>
          <label for="contact-message" class="block text-sm text-gray-300 mb-1">Message</label>
          <textarea
            id="contact-message"
            v-model.trim="message"
            class="w-full min-h-[140px] rounded-md bg-gray-800 border border-gray-700 focus:border-gray-500 focus:outline-none px-3 py-2 text-gray-100 placeholder-gray-500 resize-y"
            placeholder="Your ideas, suggestions or questions..."
            :disabled="submitting"
            required
          />
          <p v-if="messageError" class="mt-1 text-xs text-red-400">{{ messageError }}</p>
        </div>

        <button
          type="submit"
          class="w-full px-4 py-2 rounded-md bg-white/10 hover:bg-white/20 text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="submitting"
        >
          <span v-if="!submitting">Send</span>
          <span v-else>Sending...</span>
        </button>

        <p v-if="successMessage" class="text-sm text-emerald-400 text-center">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-sm text-red-400 text-center">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';
import isEmail from 'validator/lib/isEmail';


const email = ref('');
const message = ref('');
const submitting = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const emailError = ref('');
const messageError = ref('');



function validate() {
  emailError.value = '';
  messageError.value = '';

  if (!email.value) {
    emailError.value = 'Enter your email.';
  }
  else if (!isEmail(email.value)) {
    emailError.value = 'Invalid email format.';
  }

  if (!message.value) {
    messageError.value = 'Enter your message.';
  }
  else if (message.value.length < 10) {
    messageError.value = 'Message must contain at least 10 characters.';
  }

  return !emailError.value && !messageError.value;
}

async function onSubmit() {
  successMessage.value = '';
  errorMessage.value = '';

  if (!validate()) {
    return;
  }

  submitting.value = true;
  try {
    await api.post('/api/contact-us/', {
      email: email.value,
      message: message.value,
    });

    successMessage.value = 'Thank you! Your message has been sent.';
    email.value = '';
    message.value = '';
  }
  catch (e) {
    errorMessage.value = 'Failed to send. Please try again later.';
  }
  finally {
    submitting.value = false;
  }
}
</script> 