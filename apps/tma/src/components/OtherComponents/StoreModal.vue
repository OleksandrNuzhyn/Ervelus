<template>
  <Teleport to="body">
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="isOpen && !showSuccessModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-md" @click.self="$emit('close')">
        <div class="relative w-full max-w-lg md:max-w-xl h-auto max-h-[85vh] m-4 bg-[#1c1c1e]/80 backdrop-blur-xl border border-white/[0.02] rounded-2xl overflow-hidden flex flex-col shadow-2xl z-10 pointer-events-auto">
          <div class="px-6 py-5 flex items-center justify-center shrink-0">
            <h2 class="text-xl font-bold text-white tracking-tight inter w-full text-center">{{ $t('store.title') }}</h2>
          </div>

          <div class="flex-1 overflow-y-auto px-6 pb-6 space-y-6 no-scrollbar">
            <section>
              <h3 class="text-sm font-medium text-white/60 mb-4 text-center inter">{{ $t('store.free_bonuses') }}</h3>
              <div class="flex gap-3">
                
                <button class="relative flex-1 min-w-0 aspect-square rounded-2xl p-4 flex flex-col justify-between items-start bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.02] transition-all group text-left active:scale-95 shadow-lg overflow-hidden">
                  <div class="absolute -right-4 -top-4 w-24 h-24 bg-white/[0.02] rounded-full blur-2xl pointer-events-none group-hover:bg-white/[0.05] transition-colors"></div>
                  
                  <div class="mb-2 group-hover:scale-110 transition-transform duration-300">
                    <svg class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M5.25 6.375a4.125 4.125 0 1 1 8.25 0 4.125 4.125 0 0 1-8.25 0ZM2.25 19.125a7.125 7.125 0 0 1 14.25 0v.003l-.001.119a.75.75 0 0 1-.363.63 13.067 13.067 0 0 1-6.761 1.873c-2.472 0-4.786-.684-6.76-1.873a.75.75 0 0 1-.364-.63l-.001-.122ZM18.75 7.5a.75.75 0 0 0-1.5 0v2.25H15a.75.75 0 0 0 0 1.5h2.25v2.25a.75.75 0 0 0 1.5 0v-2.25H21a.75.75 0 0 0 0-1.5h-2.25V7.5Z" />
                    </svg>
                  </div>
                  <div class="relative z-10">
                    <span class="block text-3xl font-bold text-white mb-1 tracking-tighter inter">+2</span>
                    <span class="text-[11px] font-semibold text-white/60 tracking-tight whitespace-nowrap block inter">{{ $t('store.invite_friend') }}</span>
                  </div>
                </button>
    
                <button class="relative flex-1 min-w-0 aspect-square rounded-2xl p-4 flex flex-col justify-between items-start bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.02] transition-all group text-left active:scale-95 shadow-lg overflow-hidden">
                   <div class="absolute -right-4 -top-4 w-24 h-24 bg-blue-500/[0.02] rounded-full blur-2xl pointer-events-none group-hover:bg-blue-500/[0.05] transition-colors"></div>
    
                    <svg class="w-8 h-8 text-white transition-transform duration-300 group-hover:scale-110" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="16" cy="16" r="14" fill="currentColor"></circle>
                      <path d="M22.9866 10.2088C23.1112 9.40332 22.3454 8.76755 21.6292 9.082L7.36482 15.3448C6.85123 15.5703 6.8888 16.3483 7.42147 16.5179L10.3631 17.4547C10.9246 17.6335 11.5325 17.541 12.0228 17.2023L18.655 12.6203C18.855 12.4821 19.073 12.7665 18.9021 12.9426L14.1281 17.8646C13.665 18.3421 13.7569 19.1512 14.314 19.5005L19.659 22.8523C20.2585 23.2282 21.0297 22.8506 21.1418 22.1261L22.9866 10.2088Z" fill="#121214"></path>
                    </svg>
                  <div class="relative z-10">
                    <span class="block text-3xl font-bold text-white mb-1 tracking-tighter inter">+1</span>
                    <span class="text-[11px] font-semibold text-white/60 tracking-tight whitespace-nowrap block inter">{{ $t('store.join_channel') }}</span>
                  </div>
                </button>
              </div>
            </section>
    
            <section v-if="loading || starPackages.length > 0">
               <h3 class="text-sm font-medium text-white/60 mb-4 text-center inter">{{ $t('store.star_packages') }}</h3>
               <div class="flex flex-col gap-3">
                  <template v-if="loading && starPackages.length === 0">
                    <div v-for="i in 2" :key="'skeleton-'+i" class="bg-white/[0.03] border border-white/[0.02] rounded-2xl min-h-[96px] box-border animate-pulse"></div>
                  </template>
                  <template v-else-if="starPackages.length > 0">
                    <div v-for="(pkg, index) in starPackages" :key="pkg.id" 
                         class="group rounded-2xl p-4 flex items-center gap-4 transition-all duration-200 active:scale-[0.99] cursor-pointer min-h-[96px] box-border"
                         :class="index === 1 ? 'bg-gradient-to-br from-amber-500/[0.1] via-amber-500/[0.03] to-transparent border border-amber-500/20 shadow-[0_0_20px_rgba(245,158,11,0.03)]' : 'bg-gradient-to-br from-[#8774e1]/[0.1] via-[#8774e1]/[0.03] to-transparent border border-[#8774e1]/20 shadow-[0_0_20px_rgba(135,116,225,0.03)] hover:from-[#8774e1]/[0.15]'">
                       
                       <div class="flex-1 min-w-0 flex flex-col items-start gap-1">
                          <h4 class="text-[15px] font-bold tracking-tight inter leading-tight mb-0.5" :class="index === 1 ? 'text-amber-100' : 'text-[#eae5ff]'">{{ pkg.name }}</h4>
                          
                          <div class="flex items-start gap-1.5 min-w-0 w-full">
                             <svg class="w-3.5 h-3.5 shrink-0 mt-0.5" :class="index === 1 ? 'text-amber-500/70' : 'text-[#8774e1]/70'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                             </svg>
                             <p class="text-[12px] font-medium inter leading-tight tracking-tight" :class="index === 1 ? 'text-amber-100/70' : 'text-[#eae5ff]/70'">{{ pkg.generations_count }} {{ $t('store.generations') }}</p>
                          </div>

                          <div class="flex items-start gap-1.5 min-w-0 w-full">
                             <svg class="w-3.5 h-3.5 shrink-0 mt-0.5" :class="index === 1 ? 'text-amber-500/70' : 'text-[#8774e1]/70'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                             </svg>
                             <p class="text-[12px] font-medium inter leading-tight tracking-tight" :class="index === 1 ? 'text-amber-100/70' : 'text-[#eae5ff]/70'">{{ $t('store.premium_styles') }}</p>
                          </div>
                       </div>

                       <button class="shrink-0 h-9 w-[90px] flex items-center justify-center font-bold tracking-wide rounded-full transition-all active:scale-95 ml-auto gap-1 text-black"
                               :class="index === 1 ? 'bg-amber-100 hover:bg-amber-50' : 'bg-[#eae5ff] hover:bg-[#dcd6ff]'"
                               @click="createStarInvoice(pkg)">
                          {{ pkg.stars_count }}
                          <svg class="w-3.5 h-3.5 fill-current text-[#EA580C]" viewBox="0 0 14 15">
                             <path fill-rule="evenodd" clip-rule="evenodd" d="M6.63869 12.1902L3.50621 14.1092C3.18049 14.3087 2.75468 14.2064 2.55515 13.8807C2.45769 13.7216 2.42864 13.5299 2.47457 13.3491L2.95948 11.4405C3.13452 10.7515 3.60599 10.1756 4.24682 9.86791L7.6642 8.22716C7.82352 8.15067 7.89067 7.95951 7.81418 7.80019C7.75223 7.67116 7.61214 7.59896 7.47111 7.62338L3.66713 8.28194C2.89387 8.41581 2.1009 8.20228 1.49941 7.69823L0.297703 6.69116C0.00493565 6.44581 -0.0335059 6.00958 0.211842 5.71682C0.33117 5.57442 0.502766 5.48602 0.687982 5.47153L4.35956 5.18419C4.61895 5.16389 4.845 4.99974 4.94458 4.75937L6.36101 1.3402C6.5072 0.987302 6.91179 0.819734 7.26469 0.965925C7.43413 1.03612 7.56876 1.17075 7.63896 1.3402L9.05539 4.75937C9.15496 4.99974 9.38101 5.16389 9.6404 5.18419L13.3322 5.47311C13.713 5.50291 13.9975 5.83578 13.9677 6.2166C13.9534 6.39979 13.8667 6.56975 13.7269 6.68896L10.9114 9.08928C10.7131 9.25826 10.6267 9.52425 10.6876 9.77748L11.5532 13.3733C11.6426 13.7447 11.414 14.1182 11.0427 14.2076C10.8642 14.2506 10.676 14.2208 10.5195 14.1249L7.36128 12.1902C7.13956 12.0544 6.8604 12.0544 6.63869 12.1902Z" fill="currentColor"></path>
                            </svg>
                         </button>
                    </div>
                  </template>
               </div>
            </section>
          </div>
          <div class="p-6 pt-0 mt-auto shrink-0 z-20">
            <button @click="$emit('close')" class="w-full bg-white/[0.08] hover:bg-white/[0.12] active:scale-[0.98] transition-all text-white font-bold rounded-xl py-3.5 text-[15px] inter">
              {{ $t('navigation.close') }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="modal-fade">
      <div v-if="showErrorModal" class="fixed inset-0 flex items-center justify-center z-[110] confirm-modal-overlay" @click.self="showErrorModal = false">
        <div class="profile-card !bg-white/[0.08] !backdrop-blur-[30px] !p-10 w-11/12 max-w-md min-h-[220px] flex flex-col items-center justify-center gap-8 text-gray-200 relative">
          <div class="text-center">
            <h3 class="text-xl font-bold text-gray-200 tracking-wide mb-2">{{ $t('store.error_title') }}</h3>
            <p class="text-[15px] text-white/50 leading-relaxed font-medium">{{ $t('store.error_desc') }}</p>
          </div>
          <div class="flex justify-center pt-2 w-full">
            <button 
              @click="showErrorModal = false" 
              class="flex items-center justify-center h-[48px] min-w-[140px] px-6 text-[14px] font-bold rounded-2xl transition-all duration-300 bg-white/20 border border-white/[0.02] text-white hover:bg-white/30 active:scale-[0.98]"
            >
              {{ $t('navigation.close') }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="modal-fade">
      <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center z-[110] confirm-modal-overlay" @click.self="showSuccessModal = false">
        <div class="relative w-11/12 max-w-sm overflow-hidden rounded-2xl border border-white/10 bg-[#1c1c1e]/90 p-8 text-center backdrop-blur-xl shadow-2xl transition-all">
          <div class="pointer-events-none absolute -left-10 -top-10 h-32 w-32 rounded-full bg-green-500/20 blur-3xl"></div>
          <div class="pointer-events-none absolute -bottom-10 -right-10 h-32 w-32 rounded-full bg-emerald-500/10 blur-3xl"></div>

          <div class="relative z-10 flex flex-col items-center">
            <div class="relative mb-6 flex h-20 w-20 items-center justify-center">
              <div class="absolute inset-0 rounded-full bg-green-500/20 blur-xl"></div>
              <div class="relative flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-tr from-green-500 to-emerald-600 shadow-lg shadow-emerald-500/30">
                <svg class="h-6 w-6 text-white drop-shadow-md" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>

            <h3 class="mb-3 text-2xl font-bold tracking-tight text-white">{{ $t('store.success_title') }}</h3>
            
            <p class="mb-8 text-[15px] font-medium leading-relaxed text-white/60 whitespace-nowrap">
              {{ $t('store.success_desc') }}
            </p>

            <button 
              @click="handleSuccessClose" 
              class="group relative flex w-full items-center justify-center overflow-hidden rounded-xl bg-white text-[15px] font-bold text-black shadow-lg transition-transform active:scale-[0.98]"
            >
              <div class="absolute inset-0 bg-gradient-to-r from-gray-100 to-white opacity-100 transition-opacity group-hover:opacity-90"></div>
              <span class="relative py-3.5">{{ $t('store.got_it') }}</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue';
import api from '@/services/api';

const starPackages = ref([]);
const loading = ref(false);
const showErrorModal = ref(false);
const showSuccessModal = ref(false);

async function createStarInvoice(pkg) {
  try {
    const response = await api.post('/api/payments/create-star-invoice-link/', {
      star_package_id: pkg.id
    });
    
    if (response.data?.star_invoice_link) {
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.openInvoice(response.data.star_invoice_link, (status) => {
          if (status === 'paid') {
            showSuccessModal.value = true;
          }
        });
      }
      else {
        showErrorModal.value = true;
      }
    }
    else {
      showErrorModal.value = true;
    }
  }
  catch (e) {
    showErrorModal.value = true;
  }
}

async function getStarPackages() {
  loading.value = true;
  try {
    const { data } = await api.get('/api/products/star-packages/');
    const packages = data.star_packages || [];
    starPackages.value = packages.sort((a, b) => a.generations_count - b.generations_count);
  }
  catch (e) {
    starPackages.value = [];
  }
  finally {
    loading.value = false;
  }
}

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['close']);
import { useProductsStore } from '@/stores/products';

function handleSuccessClose() {
  showSuccessModal.value = false;
  const productsStore = useProductsStore();
  productsStore.getStyles();
  emit('close');
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    getStarPackages();
  }
}, { immediate: true });
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
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

.confirm-modal-overlay {
  background-color: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(22px);
}

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
</style>