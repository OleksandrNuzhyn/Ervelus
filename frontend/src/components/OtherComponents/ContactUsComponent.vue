<template>
  <div class="w-full max-w-2xl mx-auto px-4 md:px-8 pt-5 pb-10">
    <h1 class="text-3xl font-bold medieval text-center text-gray-200 mb-6">Contact Us</h1>
    <div class="form-container-card">
      <p class="text-xl text-gray-300 text-center">Leave your email and message here</p>

      <form class="mt-6 space-y-4" @submit.prevent="onSubmit" novalidate>
        <div>
          <label for="contact-email" class="block text-sm text-gray-300 mb-1">Email</label>
          <input
            id="contact-email"
            type="email"
            v-model.trim="email"
            class="w-full rounded-md bg-white/10 focus:border-gray-500 border border-white/10 focus:outline-none px-3 py-2 text-gray-100 placeholder-gray-500"
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
            v-model="message"
            maxlength="5000"
            class="w-full min-h-[140px] rounded-md bg-white/10 border border-white/10 focus:border-gray-500 focus:outline-none px-3 py-2 text-gray-100 placeholder-gray-500 resize-y"
            placeholder="Your ideas, suggestions, questions or bug reports..."
            :disabled="submitting"
            required/>
          <div class="mt-1 flex justify-between items-center">
            <p v-if="messageError" class="text-xs text-red-400">{{ messageError }}</p>
            <p class="text-xs text-gray-400 ml-auto" :class="{ 'text-red-400': message.length > 5000 }">{{ message.length }} / 5000</p>
          </div>
        </div>

        <button
          type="submit"
          class="w-full px-4 py-3 mt-2 rounded-full bg-white/10 hover:bg-white/20 text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="submitting"
        >
          <span v-if="!submitting">Send</span>
          <span v-else>Sending...</span>
        </button>
        <p v-if="successMessage" class="text-sm text-emerald-400 text-center">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-sm text-red-400 text-center">{{ errorMessage }}</p>
      </form>
    </div>

    <div class="mt-14">
      <h2 class="text-3xl font-bold medieval text-center text-gray-200 mb-4">FAQ</h2>
      <div class="divide-y divide-gray-700/50">
        <div v-for="(faq, index) in faqs" :key="index">
          <button @click="toggleFaq(index)" class="w-full flex justify-between items-center text-left py-5 focus:outline-none">
            <span class="text-lg transition-colors duration-300" :class="faq.isOpen ? 'text-gray-200' : 'text-gray-400'">{{ faq.question }}</span>
            <span class="flex-shrink-0 ml-4 flex items-center justify-center h-7 w-7 rounded-full bg-gray-900/50 text-gray-400">
              <svg v-if="!faq.isOpen" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6" /></svg>
            </span>
          </button>
          <transition
            enter-active-class="transition-all duration-700 ease-in-out"
            enter-from-class="max-h-0 opacity-0"
            enter-to-class="max-h-screen opacity-100"
            leave-active-class="transition-all duration-700 ease-in-out"
            leave-from-class="max-h-screen opacity-100"
            leave-to-class="max-h-0 opacity-0"
          >
            <div v-if="faq.isOpen" class="overflow-hidden">
              <p class="pr-12 pb-4 pt-2 text-gray-200">{{ faq.answer }}</p>
            </div>
          </transition>
        </div>
      </div>
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


const faqs = ref([
  {
    question: 'What is Ervelus?',
    answer: 'It is a service for image stylization based on artificial intelligence.',
    isOpen: false,
  },
  {
    question: 'How many subscriptions can a user have?',
    answer: 'A user can have multiple active subscriptions.',
    isOpen: false,
  },
  {
    question: 'What happens if I don\'t use my credits by the end of my subscription?',
    answer: 'Generations expire at the end of the subscription period.',
    isOpen: false,
  },
]);

const toggleFaq = (selectedIndex) => {
  const currentlyOpenIndex = faqs.value.findIndex(faq => faq.isOpen);

  if (currentlyOpenIndex === selectedIndex) {
    faqs.value[selectedIndex].isOpen = false;
    return;
  }

  if (currentlyOpenIndex !== -1) {
    faqs.value[currentlyOpenIndex].isOpen = false;
    faqs.value[selectedIndex].isOpen = true;
  } else {
    faqs.value[selectedIndex].isOpen = true;
  }
};



function validate() {
  emailError.value = '';
  messageError.value = '';

  if (!email.value) {
    emailError.value = 'Enter your email';
  }
  else if (!isEmail(email.value.trim())) {
    emailError.value = 'Invalid email format';
  }

  const trimmedMessage = message.value.trim();
  if (!trimmedMessage) {
    messageError.value = 'Enter your message';
  }
  else if (trimmedMessage.length < 10) {
    messageError.value = 'Message must contain at least 10 characters';
  }
  else if (message.value.length > 5000) {
    messageError.value = 'Message must be less than 5000 characters';
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
    const response = await api.post('/api/auth/support-email/send/', {
      email: email.value.trim(),
      text_body: message.value.trim(),
    });

    if (response.status === 200) {
       successMessage.value = response.data.detail;
       email.value = '';
       message.value = '';
    }
  }
  catch (e) {
    if (e.response && e.response.status === 400) {
      errorMessage.value = e.response.data.detail;
    } 
    else {
      errorMessage.value = 'An unexpected error occurred. Please try again later';
    }
  }
  finally {
    submitting.value = false;
  }
}
</script> 

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.medieval {
  font-family: 'MedievalSharp', cursive;
}

.form-container-card {
  background: rgba(255, 255, 255, 0.03);
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
  border-radius: 20px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

#contact-email:-webkit-autofill,
#contact-email:-webkit-autofill:hover,
#contact-email:-webkit-autofill:focus,
#contact-email:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 30px #374151 inset !important;
  -webkit-text-fill-color: #F3F4F6 !important;
  border: 1px solid #374151 !important;
}
</style> 