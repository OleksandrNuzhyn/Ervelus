<template>
  <transition name="modal-fade">
    <div v-if="showTermsModal" class="fixed inset-0 flex items-center justify-center z-50 confirm-modal-overlay">
      <div class="modal-content-card p-8 w-11/12 max-w-lg shadow-lg flex flex-col gap-4 text-gray-200 relative font-sans">
        <div class="pb-2">
          <h3 class="medieval text-2xl text-center text-gray-100">{{ t('terms.update_title') }}</h3>
        </div>
        <div class="text-center">
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
        <div class="flex flex-col items-center justify-center gap-4 pt-4">
          <button @click="acceptTerms" :disabled="!hasAgreed" class="manage-button" :class="{ 'opacity-50 cursor-not-allowed': !hasAgreed }">
            {{ t('terms.accept_btn') }}
          </button>
          <div v-if="errorMessage" class="text-center text-red-400 text-sm mt-8">
            <p class="mb-4">{{ errorMessage }}</p>
          </div>
        </div>
        <p class="text-xs text-gray-500 mt-10 text-center">
          {{ t('terms.refuse_desc') }}
          <button @click="deleteAccount" class="text-red-400 hover:underline focus:outline-none bg-transparent border-none p-0">{{ t('terms.delete_account_link') }}</button>
        </p>
        <div class="border-t border-white/10 text-center pt-4">
            <p class="text-xs text-gray-500 mb-2">{{ t('terms.review_docs') }}</p>
            <div class="flex justify-center gap-4">
                <a href="/terms-of-service" target="_blank" rel="noopener noreferrer" class="text-xs text-gray-400 hover:underline">{{ t('terms.tos') }}</a>
                <a href="/privacy-policy" target="_blank" rel="noopener noreferrer" class="text-xs text-gray-400 hover:underline">{{ t('terms.privacy') }}</a>
                <a href="/refund-policy" target="_blank" rel="noopener noreferrer" class="text-xs text-gray-400 hover:underline">{{ t('terms.refund') }}</a>
                <a href="/cookie-policy" target="_blank" rel="noopener noreferrer" class="text-xs text-gray-400 hover:underline">{{ t('terms.cookies') }}</a>
            </div>
        </div>
      </div>
    </div>
  </transition>
  <transition name="modal-fade">
    <div v-if="showConfirmDeleteModal" class="fixed inset-0 flex items-center justify-center z-50 confirm-modal-overlay" @click.self="handleCancelDelete">
      <div class="modal-content-card p-8 w-11/12 max-w-md shadow-lg flex flex-col gap-5 text-gray-200 relative">
        <div class="pb-2">
          <h3 class="medieval text-2xl text-center text-gray-100">{{ t('terms.delete_title') }}</h3>
        </div>
        <div class="text-center">
          <p class="text-gray-300 text-base m-0 leading-relaxed">{{ t('terms.delete_confirm') }}</p>
        </div>

        <div v-if="errorMessage" class="text-center text-red-400 text-sm">
          <p class="mb-4">{{ errorMessage }}</p>
        </div>

        <div class="flex justify-center gap-4 pt-2">
          <button @click="handleCancelDelete" class="delete-button-subtle small-manage-button">
            {{ t('terms.cancel_btn') }}
          </button>
          <button @click="handleConfirmDelete" class="manage-button small-manage-button">
            {{ t('terms.confirm_btn') }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed } from 'vue';
import { showTermsModal, requiredAgreements, hide } from '@/services/terms';
import { useAuthStore } from '@/stores/auth';
import { toast } from '@/services/toast';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const authStore = useAuthStore();
const router = useRouter();

const hasAgreed = ref(false);
const showConfirmDeleteModal = ref(false);
const errorMessage = ref('');

let confirmActionResolve = null;

const documentTypes = computed(() => {
  const getLabel = (type) => {
    const map = {
      'terms_of_service': t('terms.tos'),
      'privacy_policy': t('terms.privacy'),
      'refund_policy': t('terms.refund'),
      'cookie_policy': t('terms.cookies')
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

async function deleteAccount() {
  errorMessage.value = '';
  showConfirmDeleteModal.value = true;

  const confirmed = await new Promise(resolve => {
    confirmActionResolve = resolve;
  });

  if (confirmed) {
    try {
      await api.delete('/api/auth/account/delete/');
      toast.info(t('terms.success_delete'));
      hide();
      authStore.user = null;
      authStore.authChecked = true;
      localStorage.removeItem('user-token');
      router.push({ name: 'home' });
    }
    catch (error) {
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage.value = error.response.data.detail;
      }
      else {
        errorMessage.value = t('terms.error_delete_failed');
      }
    }
    finally {
      confirmActionResolve = null;
    }
  }
}

function handleConfirmDelete() {
  if (confirmActionResolve) {
    confirmActionResolve(true);
    showConfirmDeleteModal.value = false;
  }
}

function handleCancelDelete() {
  if (confirmActionResolve) {
    confirmActionResolve(false);
    showConfirmDeleteModal.value = false;
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

.delete-button-subtle {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #9ca3af;
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.delete-button-subtle:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  border-color: rgba(239, 68, 68, 0.4);
}

.small-manage-button {
  min-width: 0;
  padding: 0.5rem 1.5rem;
  font-size: 0.9rem;
}
</style>