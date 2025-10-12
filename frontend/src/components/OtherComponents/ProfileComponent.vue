<template>
  <div :class="{'animations-paused': !animationsEnabled}" class="p-3 text-white h-full flex flex-col font-sans profile-container">
    <transition name="fade">
      <div v-if="!isLoading" class="flex-grow flex flex-col w-full max-w-[1850px] mx-auto space-y-8">
        <div class="py-2 flex-grow flex flex-col items-center">
          <div class="w-full max-w-2xl pt-5">
            <div class="relative z-10 flex flex-col h-full">
              <h2 class="text-3xl font-semibold text-gray-200 mb-6 medieval text-center">Subscriptions</h2>
              
              <div v-if="subscriptions.length > 0" class="space-y-6 pb-6">
                <div v-for="sub in subscriptions" :key="sub.id" class="single-subscription-card">
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
                <div class="single-subscription-card flex flex-col items-center justify-center text-center text-gray-400">
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

const authStore = useAuthStore();
const router = useRouter();

const subscriptions = ref([]);
const portalUrl = ref('');
const isLoading = ref(true);
const errorMessage = ref('');
const animationsEnabled = ref(false);
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
    subscriptions.value = response.data.subscriptions;
    portalUrl.value = response.data.portal_url;
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
      router.push({ name: 'home' });
      authStore.logout();
    }
    catch (error) {
      if (error.response && error.response.status === 400 && error.response.data && error.response.data.detail) {
        errorMessage.value = error.response.data.detail;
      }
      else {
        errorMessage.value = 'An unexpected error occurred while deleting your account';
      }
    }
  }
}

const handleConfirm = () => {
  if (confirmActionResolve) {
    confirmActionResolve(true);
    showConfirmModal.value = false;
  }
};

const handleCancel = () => {
  if (confirmActionResolve) {
    confirmActionResolve(false);
    showConfirmModal.value = false;
  }
};

function formatDateTime(dateString) {
  if (!dateString) return 'None';
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  };
  return new Date(dateString).toLocaleString(undefined, options);
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
  setTimeout(() => {
    animationsEnabled.value = true;
  }, 1500);
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

.animations-paused::before,
.animations-paused::after {
  animation-play-state: paused !important;
}

.profile-container::before {
    content: '';
    position: absolute;
    top: -40%;
    left: -40%;
    width: 180%;
    height: 180%;
    z-index: 0;
    transform: translateZ(0);
    background: 
        radial-gradient(ellipse 800px 200px at 2% 10%, rgba(129, 180, 253, 0.22) 0%, transparent 60%),
        radial-gradient(ellipse 200px 900px at 98% 2%, rgba(147, 226, 252, 0.18) 0%, transparent 55%),
        radial-gradient(ellipse 1000px 300px at 10% 95%, rgba(168, 213, 253, 0.17) 0%, transparent 68%),
        radial-gradient(ellipse 300px 1000px at 90% 98%, rgba(129, 180, 253, 0.20) 0%, transparent 50%),
        radial-gradient(ellipse 700px 400px at 30% -5%, rgba(147, 226, 252, 0.15) 0%, transparent 70%),
        radial-gradient(ellipse 400px 700px at -5% 80%, rgba(168, 213, 253, 0.13) 0%, transparent 60%),
        radial-gradient(ellipse 900px 250px at 70% 15%, rgba(129, 180, 253, 0.16) 0%, transparent 65%),
        radial-gradient(ellipse 250px 900px at 20% 70%, rgba(147, 226, 252, 0.13) 0%, transparent 58%),
        radial-gradient(ellipse 600px 350px at 85% 60%, rgba(168, 213, 253, 0.18) 0%, transparent 62%),
        radial-gradient(ellipse 350px 600px at 50% 30%, rgba(129, 180, 253, 0.13) 0%, transparent 60%),
        radial-gradient(ellipse 700px 400px at 15% 45%, rgba(147, 226, 252, 0.15) 0%, transparent 70%),
        radial-gradient(ellipse 400px 700px at 75% 5%, rgba(168, 213, 253, 0.17) 0%, transparent 65%),
        radial-gradient(ellipse 800px 300px at 5% 50%, rgba(129, 180, 253, 0.14) 0%, transparent 60%),
        radial-gradient(ellipse 300px 800px at 95% 40%, rgba(147, 226, 252, 0.10) 0%, transparent 70%);
    filter: blur(50px);
    animation: chaotic-leaks-1 120s ease-in-out infinite;
}

.profile-container::after {
    content: '';
    position: absolute;
    top: -45%;
    left: -45%;
    width: 190%;
    height: 190%;
    z-index: 0;
    transform: translateZ(0);
    background: 
        radial-gradient(ellipse 900px 400px at 5% 80%, rgba(129, 180, 253, 0.10) 0%, transparent 60%),
        radial-gradient(ellipse 300px 900px at 5% 95%, rgba(129, 180, 253, 0.21) 0%, transparent 55%),
        radial-gradient(ellipse 1100px 400px at 30% 10%, rgba(168, 213, 253, 0.18) 0%, transparent 68%),
        radial-gradient(ellipse 400px 1100px at 100% 70%, rgba(129, 180, 253, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse 900px 500px at 0% 30%, rgba(147, 226, 252, 0.13) 0%, transparent 70%),
        radial-gradient(ellipse 600px 900px at 80% 0%, rgba(168, 213, 253, 0.16) 0%, transparent 60%),
        radial-gradient(ellipse 300px 700px at 20% 100%, rgba(129, 180, 253, 0.13) 0%, transparent 58%),
        radial-gradient(ellipse 800px 300px at 10% 60%, rgba(147, 226, 252, 0.17) 0%, transparent 78%),
        radial-gradient(ellipse 700px 900px at 90% 40%, rgba(168, 213, 253, 0.20) 0%, transparent 62%),
        radial-gradient(ellipse 500px 800px at 40% 70%, rgba(129, 180, 253, 0.13) 0%, transparent 60%),
        radial-gradient(ellipse 800px 500px at 25% 15%, rgba(147, 226, 252, 0.15) 0%, transparent 70%),
        radial-gradient(ellipse 500px 800px at 70% 5%, rgba(168, 213, 253, 0.17) 0%, transparent 65%),
        radial-gradient(ellipse 900px 400px at 5% 80%, rgba(129, 180, 253, 0.13) 0%, transparent 60%),
        radial-gradient(ellipse 400px 900px at 95% 30%, rgba(147, 226, 252, 0.10) 0%, transparent 70%);
    filter: blur(40px);
    animation: chaotic-leaks-2 120s ease-in-out infinite reverse;
}

@keyframes chaotic-leaks-1 {
    0% { 
        transform: translate(0%, 0%) scale(1) rotate(0deg);
        opacity: 0.77;
    }
    12% { 
        transform: translate(-8%, 5%) scale(1.1) rotate(15deg);
        opacity: 0.95;
    }
    25% { 
        transform: translate(6%, -10%) scale(0.9) rotate(-8deg);
        opacity: 0.70;
    }
    38% { 
        transform: translate(-5%, 12%) scale(1.2) rotate(25deg);
        opacity: 0.8;
    }
    50% { 
        transform: translate(10%, -7%) scale(0.85) rotate(-18deg);
        opacity: 0.75;
    }
    63% { 
        transform: translate(-9%, -3%) scale(1.05) rotate(35deg);
        opacity: 0.9;
    }
    75% { 
        transform: translate(4%, 8%) scale(0.95) rotate(-25deg);
        opacity: 0.7;
    }
    88% { 
        transform: translate(-6%, -11%) scale(1.15) rotate(12deg);
        opacity: 0.5;
    }
    100% { 
        transform: translate(0%, 0%) scale(1) rotate(0deg);
        opacity: 0.77;
    }
}

@keyframes chaotic-leaks-2 {
    0% { 
        transform: translate(0%, 0%) scale(0.95) rotate(0deg);
        opacity: 0.5;
    }
    15% { 
        transform: translate(9%, -6%) scale(1.25) rotate(-20deg);
        opacity: 0.90;
    }
    30% { 
        transform: translate(-11%, 8%) scale(0.8) rotate(30deg);
        opacity: 0.95;
    }
    45% { 
        transform: translate(5%, -13%) scale(1.1) rotate(-12deg);
        opacity: 0.3;
    }
    60% { 
        transform: translate(-8%, 4%) scale(0.9) rotate(40deg);
        opacity: 0.85;
    }
    75% { 
        transform: translate(12%, 6%) scale(1.0) rotate(-32deg);
        opacity: 0.75;
    }
    90% { 
        transform: translate(-4%, -9%) scale(1.2) rotate(22deg);
        opacity: 0.90;
    }
    100% { 
        transform: translate(0%, 0%) scale(0.95) rotate(0deg);
        opacity: 0.5;
    }
}

.single-subscription-card {
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