<template>
  <transition name="modal-fade">
    <div v-if="showTermsModal && !isPolicyPage && !isNavigating" class="fixed inset-0 flex items-center justify-center z-[100] bg-black/60 backdrop-blur-[15px]">
      <div class="solid-panel p-10 w-11/12 max-w-xl shadow-2xl flex flex-col gap-8 text-gray-200 relative">
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

        <div class="border-t border-white/[0.02] pt-6">
            <div class="grid grid-cols-2 gap-3 mb-6">
                <div @click="navigateTo('/terms-of-service')" class="cursor-pointer flex items-center justify-center text-[12px] font-medium text-white/40 hover:text-white/80 hover:bg-white/10 py-3 rounded-2xl transition-all border border-white/[0.02] bg-white/[0.03]">{{ t('terms.tos') }}</div>
                <div @click="navigateTo('/privacy-policy')" class="cursor-pointer flex items-center justify-center text-[12px] font-medium text-white/40 hover:text-white/80 hover:bg-white/10 py-3 rounded-2xl transition-all border border-white/[0.02] bg-white/[0.03]">{{ t('terms.privacy') }}</div>
                <div @click="navigateTo('/refund-policy')" class="cursor-pointer flex items-center justify-center text-[12px] font-medium text-white/40 hover:text-white/80 hover:bg-white/10 py-3 rounded-2xl transition-all border border-white/[0.02] bg-white/[0.03]">{{ t('terms.refund') }}</div>
                <div @click="navigateTo('/cookie-policy')" class="cursor-pointer flex items-center justify-center text-[12px] font-medium text-white/40 hover:text-white/80 hover:bg-white/10 py-3 rounded-2xl transition-all border border-white/[0.02] bg-white/[0.03]">{{ t('terms.cookies') }}</div>
            </div>

            <div class="flex justify-center items-center border-t border-white/[0.02] pt-4">
              <button 
                @click="confirmDeleteAccount" 
                class="text-[13px] font-medium text-red-400 hover:text-red-300 transition-colors"
              >
                {{ t('profile.delete_account') }}
              </button>
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
import { useModalStore } from '@/stores/modal';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const modalStore = useModalStore();
const hasAgreed = ref(false);
const isNavigating = ref(false);
const isDeleting = ref(false);

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
  try {
    const acceptancePromises = requiredAgreements.value.map(agreement =>
      api.post('/api/agreements/accept_user_document_version/', { terms_version_id: agreement.id })
    );
    await Promise.all(acceptancePromises);

    hide();
    window.location.reload();
  }
  catch (error) {
    modalStore.openModal({ title: t('terms.error_generic'), message: t('terms.error_accept_failed') });
  }
}

function confirmDeleteAccount() {
  modalStore.openModal({
    title: t('profile.delete_account'),
    message: t('profile.delete_account_confirm'),
    type: 'info',
    confirmText: t('gallery.confirm'),
    cancelText: t('profile.modal_cancel'),
    onConfirm: deleteAccount
  });
}

async function deleteAccount() {
  isDeleting.value = true;
  
  try {
    const languageCode = window.Telegram?.WebApp?.initDataUnsafe?.user?.language_code;
    
    await api.delete('/api/users/delete-account/', {
      data: { language_code: languageCode }
    });
    
    localStorage.removeItem('user-token');
    
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.close();
    }
    else {
        window.location.reload();
    }
  }
  catch (error) {
    modalStore.openModal({ title: t('profile.delete_account'), message: t('profile.delete_account_error') });
  }
  finally {
    isDeleting.value = false;
  }
}
</script>