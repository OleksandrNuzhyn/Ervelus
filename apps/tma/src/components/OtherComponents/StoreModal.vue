<template>
  <Teleport to="body">
    <transition name="modal-fade">
      <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-[15px]" @click.self="modalStore.closeStore()">
        <div class="solid-panel w-full max-w-lg md:max-w-xl relative overflow-hidden h-auto m-4 pointer-events-auto shadow-2xl">
          <div class="pointer-events-none absolute -left-10 -top-10 h-48 w-48 rounded-full bg-white/5 blur-[100px]"></div>
          <div class="pointer-events-none absolute -bottom-10 -right-10 h-48 w-48 rounded-full bg-white/5 blur-[100px]"></div>

          <div class="pt-8 pb-4 relative z-10">
            <h2 class="text-xl font-bold text-white tracking-tight inter w-full text-center">{{ $t('store.title') }}</h2>
          </div>

          <div class="px-6 pb-6 space-y-6 relative z-10">
            <section>
              <h3 class="text-sm font-medium text-white/60 mb-4 text-center inter">{{ $t('store.free_bonuses') }}</h3>
              <div class="flex flex-col gap-2.5">
                <button @click="modalStore.closeStore(); handleInviteFriend()" class="group relative flex items-center justify-between px-4 py-5 rounded-2xl bg-white/[0.04] hover:bg-white/[0.08] active:scale-[0.99] transition-all overflow-hidden w-full text-left">
                  <div class="absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  
                  <div class="relative z-10 flex flex-col gap-1 items-start min-w-0 mr-4">
                    <h4 class="text-[14px] font-bold tracking-tight inter leading-tight mb-0.5 text-white w-full">{{ $t('store.invite_friend') }}</h4>
                    <span class="text-[12px] font-medium inter leading-tight tracking-tight text-white/70 block">{{ $t('store.invite_badge') }}</span>
                  </div>

                  <div class="relative z-10 shrink-0 h-9 w-[110px] flex items-center justify-center rounded-full bg-white/[0.08] hover:bg-white/[0.12] transition-all active:scale-95 group-active:scale-95 text-white text-[13px] font-bold inter">
                    {{ $t('store.invite') }}
                  </div>
                </button>
    
                <a href="https://t.me/ervelus_news" target="_blank" @click="modalStore.closeStore()" v-if="!isSubscribed" class="group relative flex items-center justify-between px-4 py-5 rounded-2xl bg-white/[0.04] hover:bg-white/[0.08] active:scale-[0.99] transition-all overflow-hidden w-full text-left cursor-pointer no-underline">
                   <div class="absolute inset-0 bg-gradient-to-br from-blue-500/[0.05] to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>

                  <div class="relative z-10 flex flex-col gap-1 items-start min-w-0 mr-4">
                    <h4 class="text-[14px] font-bold tracking-tight inter leading-tight mb-0.5 text-white w-full">{{ $t('store.join_channel') }}</h4>
                    <span class="text-[12px] font-medium inter leading-tight tracking-tight text-white/70 block">{{ $t('store.invite_badge') }}</span>
                  </div>

                  <div class="relative z-10 shrink-0 h-9 w-[110px] flex items-center justify-center rounded-full bg-white/[0.08] hover:bg-white/[0.12] transition-all active:scale-95 group-active:scale-95 text-white text-[13px] font-bold inter">
                    {{ $t('store.subscribe') }}
                  </div>
                </a>

                <div v-else class="relative flex items-center justify-between px-4 py-5 rounded-2xl bg-emerald-500/[0.08] overflow-hidden w-full text-left">
                   <div class="absolute inset-0 bg-gradient-to-br from-emerald-500/[0.05] to-transparent"></div>

                  <div class="relative z-10 flex flex-col gap-1 items-start min-w-0 mr-4">
                    <h4 class="text-[14px] font-bold tracking-tight inter leading-tight mb-0.5 text-emerald-100 w-full">{{ $t('store.join_channel') }}</h4>
                    <span class="text-[12px] font-medium inter leading-tight tracking-tight text-emerald-100/70 block">{{ $t('store.invite_badge') }}</span>
                  </div>
                  
                  <div class="relative z-10 h-9 w-[110px] flex items-center justify-center rounded-full bg-emerald-500/20 text-emerald-300 shrink-0">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
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
                          <h4 class="text-[14px] font-bold tracking-tight inter leading-tight mb-0.5" :class="index === 1 ? 'text-amber-100' : 'text-[#eae5ff]'">{{ pkg.name }}</h4>
                          
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

                       <button class="shrink-0 h-9 w-[110px] flex items-center justify-center font-bold tracking-wide rounded-full transition-all active:scale-95 ml-auto gap-1 text-black bg-white hover:bg-gray-50 shadow-sm"
                               @click="createStarInvoice(pkg)">
                          {{ pkg.stars_count }}
                          <svg class="w-4 h-4 fill-current text-yellow-400" style="filter: drop-shadow(0px 0px 0.5px rgba(0,0,0,0.25));" viewBox="0 0 14 15">
                             <path fill-rule="evenodd" clip-rule="evenodd" d="M6.63869 12.1902L3.50621 14.1092C3.18049 14.3087 2.75468 14.2064 2.55515 13.8807C2.45769 13.7216 2.42864 13.5299 2.47457 13.3491L2.95948 11.4405C3.13452 10.7515 3.60599 10.1756 4.24682 9.86791L7.6642 8.22716C7.82352 8.15067 7.89067 7.95951 7.81418 7.80019C7.75223 7.67116 7.61214 7.59896 7.47111 7.62338L3.66713 8.28194C2.89387 8.41581 2.1009 8.20228 1.49941 7.69823L0.297703 6.69116C0.00493565 6.44581 -0.0335059 6.00958 0.211842 5.71682C0.33117 5.57442 0.502766 5.48602 0.687982 5.47153L4.35956 5.18419C4.61895 5.16389 4.845 4.99974 4.94458 4.75937L6.36101 1.3402C6.5072 0.987302 6.91179 0.819734 7.26469 0.965925C7.43413 1.03612 7.56876 1.17075 7.63896 1.3402L9.05539 4.75937C9.15496 4.99974 9.38101 5.16389 9.6404 5.18419L13.3322 5.47311C13.713 5.50291 13.9975 5.83578 13.9677 6.2166C13.9534 6.39979 13.8667 6.56975 13.7269 6.68896L10.9114 9.08928C10.7131 9.25826 10.6267 9.52425 10.6876 9.77748L11.5532 13.3733C11.6426 13.7447 11.414 14.1182 11.0427 14.2076C10.8642 14.2506 10.676 14.2208 10.5195 14.1249L7.36128 12.1902C7.13956 12.0544 6.8604 12.0544 6.63869 12.1902Z"></path>
                          </svg>
                         </button>
                    </div>
                  </template>
               </div>
            </section>
          </div>
          <div class="px-6 pb-7 pt-2 z-20">
            <button @click="modalStore.closeStore" class="w-full bg-white/[0.08] hover:bg-white/[0.12] active:scale-[0.98] transition-all text-white font-bold rounded-xl py-3.5 text-[15px] inter">
              {{ $t('navigation.close') }}
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
import { useProductsStore } from '@/stores/products';
import { useModalStore } from '@/stores/modal';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const modalStore = useModalStore();
const productsStore = useProductsStore();
const starPackages = ref([]);
const isSubscribed = ref(false);
const loading = ref(false);

async function createStarInvoice(pkg) {
  try {
    const response = await api.post('/api/payments/create-star-invoice-link/', {
      star_package_id: pkg.id
    });
    
    if (response.data?.star_invoice_link) {
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.openInvoice(response.data.star_invoice_link, (status) => {
          if (status === 'paid') {
            modalStore.closeStore();
            productsStore.getStyles();
            modalStore.openModal({
              title: t('store.success_title'),
              message: t('store.success_desc'),
              type: 'success'
            });
          }
        });
      }
      else {
        modalStore.openModal({ title: t('store.error_title'), message: t('store.error_desc') });
      }
    }
    else {
      modalStore.openModal({ title: t('store.error_title'), message: t('store.error_desc') });
    }
  }
  catch (e) {
    modalStore.openModal({ title: t('store.error_title'), message: t('store.error_desc') });
  }
}

async function handleInviteFriend() {
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.switchInlineQuery('invite', ['users', 'groups', 'channels']);
  }
  else {
    modalStore.openModal({ title: t('store.invite_friend'), message: t('workspace.share_not_supported') });
  }
}

async function getStarPackages() {
  loading.value = true;
  try {
    const { data } = await api.get('/api/products/store/');
    const packages = data.star_packages || [];
    isSubscribed.value = data.is_subscribed;
    starPackages.value = packages.sort((a, b) => a.generations_count - b.generations_count);
  }
  catch (e) {
    starPackages.value = [];
    isSubscribed.value = false;
    modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_load_failed') });
  }
  finally {
    loading.value = false;
  }
}

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['close']);

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    getStarPackages();
  }
}, { immediate: true });
</script>