<template>
  <div class="text-white h-full flex flex-col font-sans profile-container pb-6">
    <div class="noise-overlay"></div>
    <div class="ambient-light"></div>
    <div class="global-background">
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
      <div class="glow-orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>
    <div class="flex-grow flex flex-col w-full max-w-[1850px] mx-auto space-y-8 pt-3">
      <div class="py-2 flex-grow flex flex-col items-center">
          <div class="w-11/12 max-w-2xl">
            <div class="relative z-10 flex flex-col h-full">

              <div class="mb-8 flex justify-center">
                <a href="https://t.me/ervelus_bot" target="_blank"
                  class="profile-card !py-4 !px-8 min-h-[175px] w-full max-w-2xl flex flex-col items-center justify-center gap-4 transition-all duration-300 group border border-[#28A8EA]/20 hover:!border-[#28A8EA]/50 hover:bg-[#28A8EA]/5 no-underline">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram" class="w-10 h-10 flex-shrink-0 transition-transform duration-300 group-hover:scale-110" />
                  <div class="text-center w-full overflow-hidden">
                    <h3 class="text-xl font-bold text-gray-200 group-hover:text-white transition-colors leading-tight">{{ $t('profile.support_title') }}</h3>
                    <p class="text-[12px] text-gray-400 mt-1 whitespace-nowrap truncate px-2">{{ $t('profile.support_desc') }}</p>
                  </div>
                </a>
              </div>

              <div class="mb-8 flex justify-center w-full">
                <div class="profile-card !py-6 !px-8 min-h-[245px] w-full max-w-2xl flex flex-col items-center justify-center gap-6">
                  <h3 class="text-xl font-bold text-gray-200 tracking-wide">{{ $t('profile.promo_title') }}</h3>
                  
                  <div class="flex flex-col sm:flex-row items-stretch justify-center gap-3 w-full max-w-md">
                    <input 
                      v-model="promoCode" 
                      :placeholder="$t('profile.promo_placeholder')" 
                      @keyup.enter="applyPromoCode"
                      class="w-full sm:w-auto flex-grow h-[48px] bg-white/[0.04] border border-white/[0.02] rounded-2xl px-4 text-white text-[15px] placeholder:text-white/20 focus:outline-none focus:bg-white/[0.08] transition-all font-medium"
                    />
                    
                    <button 
                      @click="applyPromoCode" 
                      :disabled="!promoCode || isSubmittingPromo"
                      class="flex items-center justify-center h-[48px] min-w-[120px] px-8 text-[14px] font-bold rounded-2xl transition-all duration-300"
                      :class="!promoCode ? 'bg-white/10 text-white/40 cursor-not-allowed' : 'bg-white/25 text-white hover:bg-white/35 active:scale-[0.98]'"
                    >
                      {{ $t('profile.promo_activate') }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="w-11/12 max-w-2xl flex flex-col items-center">
            <div class="w-full profile-card !p-0 overflow-hidden min-h-[180px] flex flex-col">
              <div class="flex-grow flex flex-col justify-center w-full">
                <router-link to="/terms-of-service" class="settings-item flex items-center justify-between px-8 py-4 border-b border-white/[0.02] active:bg-white/5 transition-colors group">
                  <span class="text-white/80 font-medium text-[15px] group-hover:text-white transition-colors">{{ $t('navigation.terms') }}</span>
                  <svg width="6" height="10" viewBox="0 0 6 10" fill="none" class="opacity-20 group-hover:opacity-40 transition-opacity">
                    <path d="M1 9L5 5L1 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </router-link>
                
                <router-link to="/privacy-policy" class="settings-item flex items-center justify-between px-8 py-4 border-b border-white/[0.02] active:bg-white/5 transition-colors group">
                  <span class="text-white/80 font-medium text-[15px] group-hover:text-white transition-colors">{{ $t('navigation.privacy') }}</span>
                  <svg width="6" height="10" viewBox="0 0 6 10" fill="none" class="opacity-20 group-hover:opacity-40 transition-opacity">
                    <path d="M1 9L5 5L1 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </router-link>
                
                <router-link to="/refund-policy" class="settings-item flex items-center justify-between px-8 py-4 border-b border-white/[0.02] active:bg-white/5 transition-colors group">
                  <span class="text-white/80 font-medium text-[15px] group-hover:text-white transition-colors">{{ $t('navigation.refund') }}</span>
                  <svg width="6" height="10" viewBox="0 0 6 10" fill="none" class="opacity-20 group-hover:opacity-40 transition-opacity">
                    <path d="M1 9L5 5L1 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </router-link>
                
                <router-link to="/cookie-policy" class="settings-item flex items-center justify-between px-8 py-4 active:bg-white/5 transition-colors group">
                  <span class="text-white/80 font-medium text-[15px] group-hover:text-white transition-colors">{{ $t('navigation.cookie') }}</span>
                  <svg width="6" height="10" viewBox="0 0 6 10" fill="none" class="opacity-20 group-hover:opacity-40 transition-opacity">
                    <path d="M1 9L5 5L1 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </router-link>
              </div>

              <div class="py-4 flex items-center justify-center w-full border-t border-white/[0.02] bg-white/[0.03]">
                <p class="text-[11px] text-white/30 text-center font-medium tracking-wide m-0">
                  &copy; {{ year }} Ervelus. {{ $t('navigation.rights_reserved') }}
                </p>
              </div>
            </div>
          </div>
      </div>
    </div>

    <transition name="modal-fade">
      <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50 confirm-modal-overlay" @click.self="showModal = false">
        <div class="profile-card !bg-white/[0.08] !backdrop-blur-[30px] !p-10 w-11/12 max-w-md min-h-[220px] flex flex-col items-center justify-center gap-8 text-gray-200 relative">
          <div class="text-center">
            <h3 class="text-xl font-bold text-gray-200 tracking-wide mb-2">{{ modalTitle }}</h3>
            <p class="text-[15px] text-white/50 leading-relaxed font-medium">{{ modalMessage }}</p>
          </div>
          <div class="flex justify-center pt-2 w-full">
            <button 
              @click="showModal = false" 
              class="flex items-center justify-center h-[48px] min-w-[160px] px-8 text-[14px] font-bold rounded-2xl transition-all duration-300 bg-white/20 border border-white/[0.02] text-white hover:bg-white/30 active:scale-[0.98]"
            >
              {{ $t('profile.modal_got_it') }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const year = new Date().getFullYear();
const promoCode = ref('');
const isSubmittingPromo = ref(false);

const showModal = ref(false);
const modalTitle = ref('');
const modalMessage = ref('');

function openModal(title, message) {
  modalTitle.value = title;
  modalMessage.value = message;
  showModal.value = true;
}

async function applyPromoCode() {
  if (!promoCode.value || isSubmittingPromo.value) return;
  
  isSubmittingPromo.value = true;
  try {
    const response = await api.post('/api/marketing/promo-codes/', { code: promoCode.value });
    openModal(t('profile.alert_success'), t('profile.alert_promo_applied', { count: response.data.credits_count }));
    promoCode.value = '';
  }
  catch (error) {
    const msg = error.response?.data?.detail || t('profile.alert_promo_failed');
    openModal(t('profile.alert_promo_error'), msg);
  }
  finally {
    isSubmittingPromo.value = false;
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.profile-container {
  position: relative;
  overflow: hidden;
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
  padding: 2.5rem;
  position: relative;
  display: flex;
  flex-direction: column;
}

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
  border: 1px solid rgba(255, 255, 255, 0.02);
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
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.02);
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

.settings-item:active svg {
  opacity: 0.6;
  transform: translateX(2px);
  transition: transform 0.2s ease;
}

.noise-overlay {
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 1;
  opacity: 0.3;
  display: block;
}

.ambient-light {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 0%, rgba(139, 180, 255, 0.08), transparent 70%);
  pointer-events: none;
  z-index: 2;
  display: block; 
}

.global-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background-color: #0c0d14;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.2;
  mix-blend-mode: screen;
  display: block;
}

.orb-1 {
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  top: -200px;
  left: -200px;
  opacity: 1;
  filter: blur(80px); 
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: #94a3b8;
  bottom: -100px;
  right: -100px;
  opacity: 0.1;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.2);
  top: 40%;
  left: 40%;
  opacity: 0.1;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(circle at 50% 40%, black 60%, transparent 100%);
  opacity: 0.7;
  filter: brightness(1.7);
  display: block;
}
</style>