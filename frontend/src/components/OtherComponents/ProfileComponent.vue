<template>
  <div class="p-3 text-white h-full flex flex-col font-sans profile-container">
    <transition name="fade">
      <div v-if="!isLoading" class="flex-grow flex flex-col w-full max-w-[1850px] mx-auto space-y-8">
        <div class="py-2 flex-grow flex flex-col items-center">
          <div class="w-full max-w-2xl pt-5">
            <div class="relative z-10 flex flex-col h-full">
              <h2 class="text-3xl font-semibold text-gray-200 mb-6 medieval text-center">Subscriptions</h2>
              
              <div v-if="subscriptions.length > 0" class="space-y-6 pb-6">
                <div v-for="sub in subscriptions" :key="sub.id" class="subscription-display-card">
                  <div class="relative z-10 flex flex-col h-full">
                    <div>
                      <div class="flex justify-between items-baseline">
                        <h3 class="text-2xl font-bold text-gray-100 medieval">{{ sub.plan_name }}</h3>
                        <p class="text-2xl font-semibold medieval">${{ sub.plan_price }}<span class="text-sm text-gray-400 font-normal">/month</span></p>
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
                          <p class="text-sm text-gray-400 mt-2">Credits Remaining</p>
                      </div>
                      <div class="flex justify-around text-center">
                          <div>
                              <p class="text-2xl font-semibold">{{ sub.plan_generations_count }}</p>
                              <p class="text-sm text-gray-400 mt-2">Generations/month</p>
                          </div>
                          <div>
                              <p class="text-2xl font-semibold">{{ sub.plan_unlocked_styles_count }}</p>
                              <p class="text-sm text-gray-400 mt-2">Unlocked Styles</p>
                          </div>
                      </div>
                    </div>
                    
                    <div>
                      <div class="pt-6 text-gray-400 text-sm">
                        <div class="text-center space-y-4">
                          <div>
                            <p class="text-xs text-gray-500 mb-1">From:</p>
                            <p class="text-sm">{{ formatDateTime(sub.start_time) }}</p>
                          </div>
                          <div>
                            <p class="text-xs text-gray-500 mb-1">Until:</p>
                            <p class="text-sm">{{ formatDateTime(sub.end_time) }}</p>
                          </div>
                        </div>
                      </div>
                      
                      <div class="mt-8">
                        <div class="flex justify-center">
                          <a v-if="portalUrl" :href="portalUrl" target="_blank" rel="noopener noreferrer" class="manage-button">
                            Manage Subscription
                          </a>
                          <span v-else class="manage-button opacity-50 cursor-not-allowed">
                            Manage Subscription
                          </span>
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
                    <h3 class="text-lg text-gray-300">No Subscriptions Found</h3>
                    <p class="max-w-xs mt-2 text-sm text-gray-500">No subscription plans. View our pricing options</p>
                    <router-link to="/pricing" class="manage-button mt-8">View Plans</router-link>
                  </div>
                </div>
              </div>

              <div class="mt-8 text-center">
                <p class="text-sm text-gray-400">{{ displayEmail }}</p>

                <div v-if="errorMessage" class="mt-4 text-red-400 text-sm">
                  <p>{{ errorMessage }}</p>
                </div>

                <button @click="deleteAccount" class="delete-button-subtle mt-4">
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
    <transition name="modal-fade">
      <div v-if="showConfirmModal" class="fixed inset-0 flex items-center justify-center z-50 confirm-modal-overlay" @click.self="handleCancel">
        <div class="modal-content-card p-8 w-11/12 max-w-md shadow-lg flex flex-col gap-5 text-gray-200 relative">
          <div class="pb-2">
            <h3 class="medieval text-2xl text-center text-gray-100">Delete Account</h3>
          </div>
          <div class="text-center">
            <p class="text-gray-300 text-base m-0 leading-relaxed">Are you sure you want to delete your account? This action cannot be undone</p>
          </div>
          <div class="flex justify-center gap-4 pt-4">
            <button @click="handleConfirm" class="manage-button small-manage-button">
              Confirm
            </button>
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
import { toast } from '@/services/toast';

const authStore = useAuthStore();
const router = useRouter();

const subscriptions = ref([]);
const portalUrl = ref('');
const isLoading = ref(true);
const errorMessage = ref('');
const showConfirmModal = ref(false);
const displayEmail = ref(null);
let confirmActionResolve = null;

async function getProfileData() {
  isLoading.value = true;
  errorMessage.value = '';

  if (authStore.user?.email) {
    displayEmail.value = authStore.user.email;
  }
  
  try {
    const response = await api.get('/api/subscriptions/user-subscriptions/');
    subscriptions.value = response.data?.subscriptions || [];
    portalUrl.value = response.data?.portal_url || '';
  }
  catch (error) {
    errorMessage.value = 'Could not load your subscription data. Please try again later';
  }
  finally {
    isLoading.value = false;
  }
}

async function deleteAccount() {
  errorMessage.value = '';
  showConfirmModal.value = true;

  const confirmed = await new Promise(resolve => {
    confirmActionResolve = resolve;
  });

  if (confirmed) {
    try {
      await api.delete('/api/auth/account/delete/');
      toast.info('Your account has been successfully deleted');
      await authStore.logout();
      router.push({ name: 'home' });
    }
    catch (error) {
      if (error.response && error.response.status === 400 && error.response.data && error.response.data.detail) {
        errorMessage.value = error.response.data.detail;
      }
      else {
        errorMessage.value = 'An unexpected error occurred while deleting your account';
      }
    }
    finally {
      confirmActionResolve = null;
    }
  }
}

function handleConfirm() {
  if (confirmActionResolve) {
    confirmActionResolve(true);
    showConfirmModal.value = false;
  }
}

function handleCancel() {
  if (confirmActionResolve) {
    confirmActionResolve(false);
    showConfirmModal.value = false;
  }
}

function formatDateTime(dateString) {
  if (!dateString) {
    return 'None';
  }
  return new Date(dateString).toLocaleString(undefined);
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
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
  border-radius: 20px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
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

.manage-button:hover {
  background: rgba(129, 180, 253, 0.1);
  color: #81b4fd;
  border-color: rgba(129, 180, 253, 0.4);
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
  transition: opacity 0.6s ease-out, transform 0.7s ease-out;
  will-change: opacity, transform;
  transform: translateZ(0);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(20px) translateZ(0);
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