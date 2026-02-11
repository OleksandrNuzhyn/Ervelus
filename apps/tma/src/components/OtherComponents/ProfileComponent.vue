<template>
  <div class="text-white flex flex-col font-sans profile-container pb-6">
    <div class="noise-overlay"></div>
    <div class="ambient-light"></div>
    <div class="global-background">
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
      <div class="glow-orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>
    <div class="flex-grow flex flex-col w-full max-w-[1850px] mx-auto space-y-6 pt-3">
      <div class="flex-grow flex flex-col items-center">
          <div class="w-11/12 max-w-2xl">
            <div class="relative z-10 flex flex-col h-full">

              <div class="mb-6 flex justify-center">
                <a href="https://t.me/ervelus_bot" target="_blank"
                  class="glass-card !py-4 !px-8 min-h-[175px] w-full max-w-2xl flex flex-col items-center justify-center gap-4 transition-all duration-300 group border border-[#28A8EA]/20 hover:!border-[#28A8EA]/50 hover:bg-[#28A8EA]/5 no-underline">
                  <svg class="w-10 h-10 flex-shrink-0 transition-transform duration-300 group-hover:scale-110" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <circle cx="16" cy="16" r="14" fill="url(#paint0_linear_87_7225)"></circle> <path d="M22.9866 10.2088C23.1112 9.40332 22.3454 8.76755 21.6292 9.082L7.36482 15.3448C6.85123 15.5703 6.8888 16.3483 7.42147 16.5179L10.3631 17.4547C10.9246 17.6335 11.5325 17.541 12.0228 17.2023L18.655 12.6203C18.855 12.4821 19.073 12.7665 18.9021 12.9426L14.1281 17.8646C13.665 18.3421 13.7569 19.1512 14.314 19.5005L19.659 22.8523C20.2585 23.2282 21.0297 22.8506 21.1418 22.1261L22.9866 10.2088Z" fill="white"></path> <defs> <linearGradient id="paint0_linear_87_7225" x1="16" y1="2" x2="16" y2="30" gradientUnits="userSpaceOnUse"> <stop stop-color="#37BBFE"></stop> <stop offset="1" stop-color="#007DBB"></stop> </linearGradient> </defs> </g></svg>
                  <div class="text-center w-full overflow-hidden">
                    <h3 class="text-xl font-bold text-gray-200 group-hover:text-white transition-colors leading-tight">{{ $t('profile.support_title') }}</h3>
                    <p class="text-[12px] text-gray-400 mt-1 whitespace-nowrap truncate px-2">{{ $t('profile.support_desc') }}</p>
                  </div>
                </a>
              </div>

              <div class="mb-6 flex justify-center w-full">
                <div class="glass-card !py-6 !px-8 min-h-[245px] w-full max-w-2xl flex flex-col items-center justify-center gap-6">
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
            <div class="w-full glass-card !p-0 overflow-hidden min-h-[180px] flex flex-col">
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

              <div class="w-full border-t border-white/[0.05]">
                <button @click="confirmDeleteAccount" class="settings-item flex items-center justify-between w-full px-8 py-4 active:bg-red-500/10 transition-colors group text-left">
                  <span class="text-red-400 font-medium text-[15px] group-hover:text-red-300 transition-colors">{{ $t('profile.delete_account') }}</span>
                  <svg width="6" height="10" viewBox="0 0 6 10" fill="none" class="opacity-20 group-hover:opacity-40 transition-opacity">
                    <path d="M1 9L5 5L1 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
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
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';
import { useModalStore } from '@/stores/modal';
import { useI18n } from 'vue-i18n';

const modalStore = useModalStore();
const { t } = useI18n();
const year = new Date().getFullYear();
const promoCode = ref('');
const isSubmittingPromo = ref(false);
const isDeleting = ref(false);

function confirmDeleteAccount() {
  modalStore.openModal({
    title: t('profile.delete_account'),
    message: t('profile.delete_account_confirm'),
    confirmText: t('gallery.confirm'),
    cancelText: t('profile.modal_cancel'),
    onConfirm: deleteAccount
  });
}

async function applyPromoCode() {
  if (!promoCode.value || isSubmittingPromo.value) return;
  
  isSubmittingPromo.value = true;
  try {
    const response = await api.post('/api/marketing/promo-codes/', { code: promoCode.value });
    modalStore.openModal({title: t('profile.alert_success'), message: t('profile.alert_promo_applied', { count: response.data.credits_count }), type: 'success'});
    promoCode.value = '';
  }
  catch (error) {
    const detail = String(error.response?.data?.detail || '').toLowerCase();
    let message = t('profile.alert_promo_failed');

    if (detail.includes('exist')) {
      message = t('profile.promo_not_found');
    }
    else if (detail.includes('active')) {
      message = t('profile.promo_inactive');
    }
    else if (detail.includes('limit')) {
      message = t('profile.promo_limit');
    }
    else if (detail.includes('already')) {
      message = t('profile.promo_used');
    }

    modalStore.openModal({title: t('profile.alert_promo_error'), message});
  }
  finally {
    isSubmittingPromo.value = false;
  }
}

async function deleteAccount() {
  isDeleting.value = true;
  
  try {
    await api.delete('/api/users/delete-account/');
    localStorage.removeItem('user-token');

    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.close();
    }
  }
  catch (error) {
    modalStore.openModal({title: t('profile.delete_account'), message: t('profile.delete_account_error')});
  }
  finally {
    isDeleting.value = false;
  }
}
</script>

<style scoped>


.profile-container {
  position: relative;
  overflow: hidden;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.4); }

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