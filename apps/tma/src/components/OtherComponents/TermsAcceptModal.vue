<template>
  <transition name="modal-fade">
    <div v-if="showTermsModal && !isPolicyPage && !isNavigating" class="fixed inset-0 flex items-center justify-center z-50 confirm-modal-overlay">
      <div class="modal-content-card p-8 w-11/12 max-w-lg shadow-lg flex flex-col gap-4 text-gray-200 relative font-sans">
        <div class="pb-2">
          <h3 class="medieval text-2xl text-center text-gray-100">{{ t('terms.update_title') }}</h3>
        </div>
        <div class="text-left px-1">
          <p class="text-gray-300 text-base m-0 leading-relaxed">
            {{ t('terms.update_desc', { types: documentTypes }) }}
          </p>
        </div>
        <div class="pt-4">
          <label class="flex items-center justify-center text-gray-400">
            <input type="checkbox" v-model="hasAgreed" class="mr-2 bg-gray-700 border-gray-600 rounded focus:ring-blue-500">
            <span>{{ t('terms.checkbox_label') }}</span>
          </label>
        </div>
        <div class="flex flex-col items-center justify-center gap-4 py-5">
          <button @click="acceptTerms" :disabled="!hasAgreed" class="manage-button" :class="{ 'opacity-50 cursor-not-allowed': !hasAgreed }">
            {{ t('terms.accept_btn') }}
          </button>
          <div v-if="errorMessage" class="text-center text-red-400 text-sm mt-8">
            <p class="mb-4">{{ errorMessage }}</p>
          </div>
        </div>
        <div class="border-t border-white/10 pt-4">
            <div class="grid grid-cols-2 gap-3">
                <div @click="navigateTo('/terms-of-service')" class="cursor-pointer flex items-center justify-center text-xs text-gray-400 hover:text-white hover:bg-white/5 py-2.5 rounded-lg transition-all border border-white/5 bg-white/[0.02]">{{ t('terms.tos') }}</div>
                <div @click="navigateTo('/privacy-policy')" class="cursor-pointer flex items-center justify-center text-xs text-gray-400 hover:text-white hover:bg-white/5 py-2.5 rounded-lg transition-all border border-white/5 bg-white/[0.02]">{{ t('terms.privacy') }}</div>
                <div @click="navigateTo('/refund-policy')" class="cursor-pointer flex items-center justify-center text-xs text-gray-400 hover:text-white hover:bg-white/5 py-2.5 rounded-lg transition-all border border-white/5 bg-white/[0.02]">{{ t('terms.refund') }}</div>
                <div @click="navigateTo('/cookie-policy')" class="cursor-pointer flex items-center justify-center text-xs text-gray-400 hover:text-white hover:bg-white/5 py-2.5 rounded-lg transition-all border border-white/5 bg-white/[0.02]">{{ t('terms.cookies') }}</div>
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
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.medieval {
  font-family: 'MedievalSharp', cursive;
}

.font-sans {
  font-family: 'Inter', sans-serif;
}

.confirm-modal-overlay {
  background-color: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(15px);
}

.modal-content-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
}

.manage-button {
  display: inline-block;
  width: auto;
  min-width: 270px;
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

.manage-button:hover:not(:disabled) {
  background: rgba(129, 180, 253, 0.1);
  color: #81b4fd;
  border-color: rgba(129, 180, 253, 0.4);
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>