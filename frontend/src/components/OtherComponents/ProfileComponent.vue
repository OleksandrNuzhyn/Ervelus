<template>
  <div class="p-3 text-white h-full flex flex-col font-sans profile-container">
    <transition name="fade">
      <div v-if="!isLoading" class="flex-grow flex flex-col w-full max-w-[1850px] mx-auto space-y-8">
        <div class="py-2 flex-grow flex flex-col items-center">
          <div class="w-full max-w-2xl pt-8">
            <div class="relative z-10 flex flex-col h-full">

              <div class="mb-8 flex justify-center">
                <div class="subscription-display-card !min-h-0 py-14 px-10 w-full max-w-2xl flex flex-col items-center">
                  <h3 class="medieval text-2xl font-bold text-gray-200 mb-10 tracking-wide">{{ $t('profile.promo_title') }}</h3>
                  
                  <div class="flex flex-col sm:flex-row items-center justify-center gap-10 sm:gap-4 w-full max-w-lg">
                    <input 
                      v-model="promoCode" 
                      :placeholder="$t('profile.promo_placeholder')" 
                      @keyup.enter="applyPromoCode"
                      class="w-full h-[52px] bg-transparent border border-white/10 rounded-full px-8 text-white text-lg placeholder:text-white/10 focus:outline-none focus:border-white/30 transition-all font-light flex items-center"
                    />
                    
                    <button 
                      @click="applyPromoCode" 
                      :disabled="!promoCode || isSubmittingPromo"
                      class="manage-button !h-[52px] flex items-center justify-center !min-w-[160px] !py-0 !text-base transition-all duration-300 !border-white/10"
                      :class="!promoCode ? '!text-white/10 !cursor-not-allowed grayscale' : 'opacity-100 activate-button-hover shadow-[0_0_12px_rgba(129,180,253,0.07)]'"
                    >
                      {{ $t('profile.promo_activate') }}
                    </button>
                  </div>
                </div>
              </div>

              <div v-if="subscriptions.length > 0" class="space-y-6 pb-6">
                <div v-for="sub in subscriptions" :key="sub.id" class="subscription-display-card">
                  <div class="relative z-10 flex flex-col h-full">
                    <h3 class="medieval text-2xl font-semibold text-gray-200 mb-6 text-center">{{ $t('profile.subscription_title') }}</h3>
                    <div>
                      <div class="flex justify-between items-baseline">
                        <h3 class="text-2xl font-bold text-gray-100 medieval">{{ sub.plan_name }}</h3>
                        <p class="text-2xl font-semibold medieval">${{ sub.plan_price }}<span class="text-sm text-gray-400 font-normal">{{ $t('profile.per_month') }}</span></p>
                      </div>
                      <div class="flex justify-between items-center mt-1">
                          <p class="text-gray-400 h-10 truncate flex items-center">{{ sub.plan_description }}</p>
                          <div class="flex items-center flex-shrink-0">
                              <span :class="getStatusDotClass(sub.status)" class="status-dot"></span>
                              <p class="text-gray-400 text-sm whitespace-pre-line">{{ formattedStatus(sub.status) }}</p>
                          </div>
                      </div>
                    </div>

                    <div class="my-auto py-6 border-t border-b border-white/10">
                      <div class="text-center pb-6 mb-6 border-b border-white/10">
                          <p class="text-5xl font-semibold">{{ sub.remaining_credits }}</p>
                          <p class="text-sm text-gray-400 mt-2">{{ $t('profile.credits_remaining') }}</p>
                      </div>
                      <div class="flex justify-around text-center">
                          <div>
                              <p class="text-2xl font-semibold">{{ sub.plan_generations_count }}</p>
                              <p class="text-sm text-gray-400 mt-2">{{ $t('profile.gen_per_month') }}</p>
                          </div>
                          <div>
                              <p class="text-2xl font-semibold">{{ sub.plan_unlocked_styles_count }}</p>
                              <p class="text-sm text-gray-400 mt-2">{{ $t('profile.unlocked_styles') }}</p>
                          </div>
                      </div>
                    </div>
                    
                    <div>
                      <div class="pt-6 text-gray-400 text-sm">
                        <div class="text-center space-y-4">
                          <div>
                            <p class="text-xs text-gray-500 mb-1">{{ $t('profile.from') }}</p>
                            <p class="text-sm">{{ formatDateTime(sub.start_time) }}</p>
                          </div>
                          <div>
                            <p class="text-xs text-gray-500 mb-1">{{ $t('profile.until') }}</p>
                            <p class="text-sm">{{ formatDateTime(sub.end_time) }}</p>
                          </div>
                        </div>
                      </div>
                      
                      <div class="mt-8">
                        <div class="flex justify-center">
                          <button v-if="sub.is_auto_renew" @click="cancelSubscription(sub.id)" class="manage-button">
                            {{ $t('profile.cancel_sub') }}
                          </button>
                          <button v-else disabled class="manage-button canceled-state cursor-not-allowed">
                            {{ $t('profile.canceled') }}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="pb-6">
                <div class="subscription-display-card flex flex-col items-center justify-center text-center text-gray-400">
                  <div class="relative z-10 flex flex-col h-full justify-center items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                    <h3 class="text-lg text-gray-300">{{ $t('profile.no_subs') }}</h3>
                    <p class="max-w-xs mt-2 text-sm text-gray-500">{{ $t('profile.no_subs_desc') }}</p>
                    <router-link to="/pricing" class="manage-button mt-8">{{ $t('profile.view_plans') }}</router-link>
                  </div>
                </div>
              </div>

              <div class="my-8 text-center">
                <p class="text-sm text-gray-400">{{ displayEmail }}</p>

                <button @click="deleteAccount" class="delete-button-subtle mt-4">
                  {{ $t('profile.delete_account_btn') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
    <transition name="modal-fade">
      <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50 confirm-modal-overlay" @click.self="handleModalBackdrop">
        <div class="modal-content-card p-10 w-11/12 max-w-md shadow-2xl flex flex-col gap-6 text-gray-200 relative">
          <div class="text-center">
            <h3 class="medieval text-3xl text-gray-100 mb-2">{{ modalTitle }}</h3>
            <p class="text-gray-300 text-lg mt-4 leading-relaxed">{{ modalMessage }}</p>
          </div>
          <div class="flex flex-col sm:flex-row justify-center gap-4 pt-4">
            <template v-if="isConfirmMode">
              <button @click="handleConfirm(false)" class="manage-button sm:!min-w-[140px] py-3 activate-button-hover">{{ $t('profile.modal_cancel') }}</button>
              <button @click="handleConfirm(true)" class="manage-button sm:!min-w-[140px] py-3 activate-button-hover">{{ $t('profile.modal_confirm') }}</button>
            </template>
            <template v-else>
              <button @click="showModal = false" class="manage-button sm:!min-w-[140px] py-3 activate-button-hover">{{ $t('profile.modal_got_it') }}</button>
            </template>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import { useI18n } from 'vue-i18n';

const { t, locale } = useI18n();
const authStore = useAuthStore();
const router = useRouter();

const subscriptions = ref([]);
const isLoading = ref(true);
const promoCode = ref('');
const isSubmittingPromo = ref(false);

const showModal = ref(false);
const modalTitle = ref('');
const modalMessage = ref('');
const isConfirmMode = ref(false);
const displayEmail = ref(null);
let confirmActionResolve = null;

function showAlert(title, message) {
  modalTitle.value = title;
  modalMessage.value = message;
  isConfirmMode.value = false;
  showModal.value = true;
}

async function showConfirm(title, message) {
  modalTitle.value = title;
  modalMessage.value = message;
  isConfirmMode.value = true;
  showModal.value = true;
  return new Promise(resolve => {
    confirmActionResolve = resolve;
  });
}

async function applyPromoCode() {
  if (!promoCode.value || isSubmittingPromo.value) return;
  
  isSubmittingPromo.value = true;
  try {
    const response = await api.post('/api/marketing/promo-codes/', { code: promoCode.value });
    showAlert(t('profile.alert_success'), t('profile.alert_promo_applied', { count: response.data.credits_count }));
    promoCode.value = '';
  }
  catch (error) {
    const msg = error.response?.data?.detail || t('profile.alert_promo_failed');
    showAlert(t('profile.alert_promo_error'), msg);
  }
  finally {
    isSubmittingPromo.value = false;
  }
}

async function getProfileData() {
  isLoading.value = true;

  if (authStore.user?.email) {
    displayEmail.value = authStore.user.email;
  }
  
  try {
    const response = await api.get('/api/subscriptions/user-subscriptions/');
    subscriptions.value = response.data?.subscriptions || [];
  }
  catch (error) {
    showAlert(t('profile.alert_connection_lost'), t('profile.alert_subs_failed'));
  }
  finally {
    isLoading.value = false;
  }
}

async function cancelSubscription(subscriptionId) {
  const confirmed = await showConfirm(
    t('profile.confirm_cancel_title'), 
    t('profile.confirm_cancel_msg')
  );

  if (confirmed) {
    try {
      await api.post(`/api/subscriptions/cancel-subscription/${subscriptionId}/`);
      const subscription = subscriptions.value.find(s => s.id === subscriptionId);
      if (subscription) {
        subscription.is_auto_renew = false;
      }
      showAlert(t('profile.alert_canceled_title'), t('profile.alert_canceled_msg'));
    }
    catch (error) {
       showAlert(t('profile.alert_error'), t('profile.alert_cancel_failed'));
    }
  }
}

async function deleteAccount() {
  const confirmed = await showConfirm(
    t('profile.confirm_delete_title'),
    t('profile.confirm_delete_msg')
  );

  if (confirmed) {
    try {
      await api.delete('/api/auth/account/delete/');
      authStore.user = null;
      authStore.authChecked = true;
      localStorage.removeItem('user-token');
      router.push({ name: 'home' });
    }
    catch (error) {
      const msg = error.response?.data?.detail || t('profile.alert_delete_failed');
      showAlert(t('profile.alert_error'), msg);
    }
  }
}

function handleConfirm(val) {
  if (confirmActionResolve) {
    confirmActionResolve(val);
    confirmActionResolve = null;
  }
  showModal.value = false;
}

function handleModalBackdrop() {
  if (isConfirmMode.value) {
    handleConfirm(false);
  } else {
    showModal.value = false;
  }
}

function formatDateTime(dateString) {
  if (!dateString) {
    return t('profile.none');
  }
  return new Date(dateString).toLocaleString(locale.value);
}

function getStatusDotClass(status) {
  const lowerStatus = status.toLowerCase();
  if (lowerStatus.startsWith('active')) {
    return 'dot-active';
  }
  if (lowerStatus === 'cancellation processing' || lowerStatus.startsWith('update')) {
    return 'dot-warning';
  }
  if (lowerStatus === 'canceled' || lowerStatus === 'unknown') {
    return 'dot-inactive';
  }
}

function formattedStatus(status) {
  if (status.startsWith('Update ')) {
    const words = status.split(' ');
    if (words.length >= 4) {
      return words.slice(0, 4).join(' ') + '\n' + words.slice(4).join(' ');
    }
  }
  return status;
}

onMounted(() => {
  getProfileData();
});
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

.profile-container {
  position: relative;
  overflow: hidden;
}

.subscription-display-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
  border-radius: 24px;
  padding: 2.5rem;
  position: relative;
  min-height: 585px;
  display: flex;
  flex-direction: column;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}

.dot-active { background-color: #34d399; }
.dot-warning { background-color: #fbbf24; }
.dot-inactive { background-color: #6b7280; }

.manage-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
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

.manage-button:not(:disabled):hover {
  background: rgba(129, 180, 253, 0.1);
  color: #81b4fd;
  border-color: rgba(129, 180, 253, 0.4);
  box-shadow: 0 0 15px rgba(129, 180, 253, 0.15);
}

.activate-button-hover:hover {
  background: rgba(129, 180, 253, 0.15) !important;
  color: #81b4fd !important;
  border-color: rgba(129, 180, 253, 0.4) !important;
  box-shadow: 0 0 12px rgba(129, 180, 253, 0.1);
}

.canceled-state {
  color: rgba(248, 113, 113, 0.7);
  border-color: rgba(248, 113, 113, 0.2);
  background: rgba(248, 113, 113, 0.03);
  cursor: not-allowed;
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

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.4); }

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.modal-fade-enter-from {
  opacity: 0;
  transform: translateY(20px) translateZ(0);
}

.modal-fade-leave-to {
  opacity: 0;
  transform: translateZ(0);
}

.fade-enter-active {
  transition: transform 0.7s ease-out;
  will-change: transform;
  transform: translateZ(0);
}

.fade-enter-from {
  /* No opacity change, only slide */
  transform: translateY(20px) translateZ(0);
}

@media (max-width: 1024px) {
  .fade-enter-active {
    transition: none !important;
  }
  .fade-enter-from {
    transform: none !important;
  }
}

.modal-content-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
}

.confirm-modal-overlay {
  background-color: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(15px);
}

.small-manage-button {
  min-width: 0;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}
</style>