<template>
  <transition name="modal-fade">
    <div v-if="showTermsModal && !isPolicyPage && !isNavigating" class="fixed inset-0 flex items-center justify-center z-50 confirm-modal-overlay">
      <div class="profile-card !bg-white/[0.08] !backdrop-blur-[30px] !px-6 !py-10 w-11/12 max-w-xl shadow-2xl flex flex-col gap-8 text-gray-200 relative font-sans">
        <div class="text-center w-full">
          <h3 class="text-xl font-semibold text-gray-200 tracking-wide mb-2">{{ t('terms.update_title') }}</h3>
          <p class="text-[15px] text-white/50 leading-relaxed font-medium">
            {{ t('terms.update_desc', { types: documentTypes }) }}
          </p>
        </div>

        <div class="flex flex-col items-center gap-6">
          <label class="flex items-center justify-center text-white/50 cursor-pointer group">
            <input type="checkbox" v-model="hasAgreed" class="w-4 h-4 rounded border-white/[0.02] bg-white/5 text-blue-500 focus:ring-offset-0 focus:ring-0 transition-all mr-3">
            <span class="text-sm font-medium group-hover:text-white/80 transition-colors">{{ t('terms.checkbox_label') }}</span>
          </label>

          <button 
            @click="acceptTerms" 
            :disabled="!hasAgreed" 
            class="flex items-center justify-center h-[52px] min-w-[240px] px-8 text-[15px] font-semibold rounded-2xl transition-all duration-300 active:scale-[0.98]"
            :class="!hasAgreed ? 'bg-white/10 text-white/40 cursor-not-allowed' : 'bg-white/20 border border-white/[0.05] text-white hover:bg-white/30'"
          >
            {{ t('terms.accept_btn') }}
          </button>
        </div>

        <div v-if="errorMessage" class="text-center text-red-400 text-sm -mt-2">
          <p>{{ errorMessage }}</p>
        </div>

        <div class="border-t border-white/[0.02] pt-6">
            <div class="grid grid-cols-2 gap-3">
                <div @click="navigateTo('/terms-of-service')" class="cursor-pointer flex items-center justify-center text-[12px] font-medium text-white/40 hover:text-white/80 hover:bg-white/10 py-3 rounded-2xl transition-all border border-white/[0.02] bg-white/[0.03]">{{ t('terms.tos') }}</div>
                <div @click="navigateTo('/privacy-policy')" class="cursor-pointer flex items-center justify-center text-[12px] font-medium text-white/40 hover:text-white/80 hover:bg-white/10 py-3 rounded-2xl transition-all border border-white/[0.02] bg-white/[0.03]">{{ t('terms.privacy') }}</div>
                <div @click="navigateTo('/refund-policy')" class="cursor-pointer flex items-center justify-center text-[12px] font-medium text-white/40 hover:text-white/80 hover:bg-white/10 py-3 rounded-2xl transition-all border border-white/[0.02] bg-white/[0.03]">{{ t('terms.refund') }}</div>
                <div @click="navigateTo('/cookie-policy')" class="cursor-pointer flex items-center justify-center text-[12px] font-medium text-white/40 hover:text-white/80 hover:bg-white/10 py-3 rounded-2xl transition-all border border-white/[0.02] bg-white/[0.03]">{{ t('terms.cookies') }}</div>
            </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { showTermsModal, requiredAgreements, hide } from '@/services/terms';
import api from '@/services/api';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const hasAgreed = ref(false);
const errorMessage = ref('');
const isNavigating = ref(false);

const isPolicyPage = computed(() => {
  return ['/terms-of-service', '/privacy-policy', '/refund-policy', '/cookie-policy'].includes(route.path);
});

async function navigateTo(path) {
  isNavigating.value = true;
  
  try {
    await router.push(path);
  }
  finally {
    isNavigating.value = false;
  }
}

const documentTypes = computed(() => {
  const getLabel = (type) => {
    const map = {
      'Terms of Service': t('terms.tos'),
      'Privacy Policy': t('terms.privacy')
    };
    return map[type] || type;
  };

  const names = requiredAgreements.value.map(agreement => getLabel(agreement.document_type));

  if (names.length === 1) {
    return names[0];
  }

  const andText = ` ${t('terms.and')} `;

  if (names.length === 2) {
    return names.join(andText);
  }

  return names.slice(0, -1).join(', ') + `, ${t('terms.and')} ` + names.slice(-1);
});

async function acceptTerms() {
  errorMessage.value = '';
  
  try {
    const acceptancePromises = requiredAgreements.value.map(agreement =>
      api.post('/api/agreements/accept_user_document_version/', { terms_version_id: agreement.id })
    );
    await Promise.all(acceptancePromises);

    hide();
    window.location.reload();
  }
  catch (error) {
    if (error.response?.data) {
      const data = error.response.data;
      errorMessage.value = data.message || data.detail || t('terms.error_generic');
    }
    else {
      errorMessage.value = t('terms.error_accept_failed');
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.confirm-modal-overlay {
  background-color: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(15px);
}

.profile-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.02);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
  border-radius: 16px;
  position: relative;
  display: flex;
  flex-direction: column;
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>