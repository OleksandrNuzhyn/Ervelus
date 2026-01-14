<template>
  <div class="w-full max-w-2xl mx-auto px-4 md:px-8 pt-5 pb-10">
    <h1 class="text-3xl font-bold medieval text-center text-gray-200 mb-6">{{ $t('contact.title') }}</h1>
    <a href="https://discord.gg/38NV8t57th" target="_blank"
      class="block w-full mb-6 form-container-card transition-colors duration-300 group border border-[#5865F2]/30 hover:!border-[#5865F2] hover:!bg-[#5865F2]/20 !p-4 no-underline">
      <div class="flex items-center justify-center gap-4">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
          class="text-[#5865F2] flex-shrink-0">
          <path
            d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.419-2.1569 2.419zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.419-2.1568 2.419z"
            fill="currentColor" />
        </svg>
        <div class="text-left">
          <h3 class="text-lg font-bold text-gray-100 group-hover:text-white transition-colors leading-tight">{{ $t('contact.discord_title') }}</h3>
          <p class="text-xs text-gray-400 mt-0.5">{{ $t('contact.discord_desc') }}</p>
        </div>
      </div>
    </a>

    <div class="form-container-card">
      <p class="text-xl text-gray-300 text-center">{{ $t('contact.form_desc') }}</p>
      <form class="mt-6 space-y-4" @submit.prevent="onSubmit" novalidate>
        <div>
          <label for="contact-email" class="block text-sm text-gray-300 mb-1">{{ $t('contact.email_label') }}</label>
          <input id="contact-email" type="email" v-model.trim="email"
            class="w-full rounded-md bg-white/10 focus:border-gray-500 border border-white/10 focus:outline-none px-3 py-2 text-gray-100 placeholder-gray-500"
            :placeholder="$t('contact.email_placeholder')" :disabled="submitting" required />
          <p v-if="emailError" class="mt-1 text-xs text-red-400">{{ emailError }}</p>
        </div>

        <div>
          <label for="contact-message" class="block text-sm text-gray-300 mb-1">{{ $t('contact.message_label') }}</label>
          <textarea id="contact-message" v-model="message" maxlength="5000"
            class="w-full min-h-[140px] rounded-md bg-white/10 border border-white/10 focus:border-gray-500 focus:outline-none px-3 py-2 text-gray-100 placeholder-gray-500 resize-y"
            :placeholder="$t('contact.message_placeholder')" :disabled="submitting" required />
          <div class="mt-1 flex justify-between items-center">
            <p v-if="messageError" class="text-xs text-red-400">{{ messageError }}</p>
            <p class="text-xs text-gray-400 ml-auto" :class="{ 'text-red-400': message.length > 5000 }">{{
              message.length }} / 5000</p>
          </div>
        </div>

        <button type="submit"
          class="w-full px-4 py-3 mt-2 rounded-full bg-white/10 hover:bg-white/20 text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="submitting">
          <span v-if="!submitting">{{ $t('contact.send') }}</span>
          <span v-else>{{ $t('contact.sending') }}</span>
        </button>
        <p v-if="successMessage" class="text-sm text-emerald-400 text-center">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-sm text-red-400 text-center">{{ errorMessage }}</p>
      </form>
    </div>

    <div class="mt-14">
      <h2 class="text-3xl font-bold medieval text-center text-gray-200 mb-4">{{ $t('faq.title') }}</h2>
      <div class="divide-y divide-gray-700/50">
        <div v-for="(faq, index) in faqs" :key="index">
          <button @click="toggleFaq(index)"
            class="w-full flex justify-between items-center text-left py-5 focus:outline-none">
            <span class="text-lg transition-colors duration-300"
              :class="faq.isOpen ? 'text-gray-200' : 'text-gray-400'">{{ faq.question }}</span>
            <span
              class="flex-shrink-0 ml-4 flex items-center justify-center h-7 w-7 rounded-full bg-gray-900/50 text-gray-400">
              <svg v-if="!faq.isOpen" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6" />
              </svg>
            </span>
          </button>
          <transition enter-active-class="transition-all duration-700 ease-in-out" enter-from-class="max-h-0 opacity-0"
            enter-to-class="max-h-screen opacity-100" leave-active-class="transition-all duration-700 ease-in-out"
            leave-from-class="max-h-screen opacity-100" leave-to-class="max-h-0 opacity-0">
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
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';
import isEmail from 'validator/lib/isEmail';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const email = ref('');
const message = ref('');
const submitting = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const emailError = ref('');
const messageError = ref('');

onMounted(() => {
  const authStore = useAuthStore();
  if (authStore.isAuthenticated && authStore.user.email) {
    email.value = authStore.user.email;
  }
});

const faqs = computed(() => [
  { question: t('faq.q1'), answer: t('faq.a1'), isOpen: faqStates.value[0] },
  { question: t('faq.q2'), answer: t('faq.a2'), isOpen: faqStates.value[1] },
  { question: t('faq.q3'), answer: t('faq.a3'), isOpen: faqStates.value[2] },
  { question: t('faq.q4'), answer: t('faq.a4'), isOpen: faqStates.value[3] },
  { question: t('faq.q5'), answer: t('faq.a5'), isOpen: faqStates.value[4] },
  { question: t('faq.q6'), answer: t('faq.a6'), isOpen: faqStates.value[5] },
  { question: t('faq.q7'), answer: t('faq.a7'), isOpen: faqStates.value[6] },
  { question: t('faq.q8'), answer: t('faq.a8'), isOpen: faqStates.value[7] },
  { question: t('faq.q9'), answer: t('faq.a9'), isOpen: faqStates.value[8] },
  { question: t('faq.q10'), answer: t('faq.a10'), isOpen: faqStates.value[9] },
  { question: t('faq.q11'), answer: t('faq.a11'), isOpen: faqStates.value[10] },
  { question: t('faq.q12'), answer: t('faq.a12'), isOpen: faqStates.value[11] },
  { question: t('faq.q13'), answer: t('faq.a13'), isOpen: faqStates.value[12] },
  { question: t('faq.q14'), answer: t('faq.a14'), isOpen: faqStates.value[13] },
]);

const faqStates = ref(new Array(14).fill(false));

function toggleFaq(selectedIndex) {
  const currentlyOpenIndex = faqStates.value.findIndex(state => state);

  if (currentlyOpenIndex === selectedIndex) {
    faqStates.value[selectedIndex] = false;
    return;
  }

  if (currentlyOpenIndex !== -1) {
    faqStates.value[currentlyOpenIndex] = false;
    faqStates.value[selectedIndex] = true;
  }
  else {
    faqStates.value[selectedIndex] = true;
  }
}

function validate() {
  emailError.value = '';
  messageError.value = '';

  if (!email.value) {
    emailError.value = t('contact.error_email_empty');
  }
  else if (!isEmail(email.value.trim())) {
    emailError.value = t('contact.error_email_invalid');
  }

  const trimmedMessage = message.value.trim();
  if (!trimmedMessage) {
    messageError.value = t('contact.error_message_empty');
  }
  else if (trimmedMessage.length < 10) {
    messageError.value = t('contact.error_message_min');
  }
  else if (message.value.length > 5000) {
    messageError.value = t('contact.error_message_max');
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
      errorMessage.value = t('contact.error_unexpected');
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