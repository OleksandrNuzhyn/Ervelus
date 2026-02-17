<template>
  <div :class="['flex flex-col pt-2 gap-3 relative lg:h-[calc(100vh-9.4rem)]', 
    !hasStartedTransform ? 'h-[calc(100dvh-8.6rem)] pb-3' : 'pb-21 lg:pb-2']">
    <div :class="['flex-grow flex flex-col lg:grid lg:grid-cols-2 gap-3 lg:gap-6 pb-0 overflow-visible min-h-0 lg:h-full', !hasStartedTransform ? 'h-full' : '']">
      <div :class="['flex flex-col lg:shrink overflow-visible gap-3 min-h-0', !hasStartedTransform ? 'flex-1 justify-between' : '']">
        
        <button @click="modalStore.openTips()" class="glass-card backdrop-blur-[25px] !flex-row py-2 px-4 items-center justify-center gap-2 group hover:bg-white/[0.05] transition-all cursor-pointer">
           <svg class="w-4 h-4 text-white/40 group-hover:text-white/80 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
             <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
           </svg>
           <span class="text-[12px] font-medium text-white/50 group-hover:text-white transition-colors">
             {{ $t('workspace.photo_tips_title') || 'Tips for best results' }}
           </span>
        </button>

        <div :class="['relative w-full flex flex-col lg:flex-grow overflow-visible min-h-0 lg:flex-1', !hasStartedTransform ? 'flex-1' : '']">
          <div :class="[!hasStartedTransform ? 'flex-1' : 'h-[38vh] md:h-[600px]', 'glass-card backdrop-blur-[25px] p-4 items-center justify-center w-full lg:h-full lg:flex-grow min-h-0 overflow-hidden']">
            <div v-if="!inputImageUrl" @click="triggerFileInput"
                 class="cursor-pointer w-full h-full flex flex-col items-center justify-center relative group/btn">
              
              <div class="mb-4">
                <svg class="w-16 h-16 md:w-24 md:h-24 text-white/30" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
              </div>
              <p class="text-base lg:text-xl font-medium text-white/70">{{ $t('workspace.upload_click') }}</p>
            </div>

            <div v-else @click="triggerFileInput" class="relative w-full h-full flex items-center justify-center cursor-pointer group/image" title="Click to replace image">
              <img :src="inputImageUrl" alt="Input" class="max-w-full max-h-full rounded-2xl transition-opacity duration-500" :style="{ opacity: inputImageLoaded ? 1 : 0 }" @load="onInputImageLoad" />
            </div>
            <input type="file" ref="fileInput" @change="onFileSelected" class="hidden" accept="image/jpeg, image/png, image/webp" />
          </div>
        </div>

        <button @click="onOpenStylePanel" class="glass-card backdrop-blur-[25px] !flex-row min-h-[56px] lg:min-h-[80px] py-3.5 lg:py-6 mt-0 items-center justify-center relative cursor-pointer hover:bg-white/[0.05] active:scale-[0.98] transition-all duration-300 px-4 group overflow-visible">
          <div class="flex items-center gap-2 md:gap-4 px-10 w-full justify-center min-w-0">
            <span class="text-white/70 font-medium lg:font-bold text-base lg:text-2xl shrink-0">{{ $t('workspace.style') }}</span>
            <div class="w-[1px] h-5 md:h-8 bg-white/20 shrink-0 relative top-[1px]"></div>
            <span class="font-medium lg:font-bold text-white text-base lg:text-2xl tracking-wide truncate">{{ props.selectedStyleName }}</span>
          </div>
          <svg class="absolute right-5 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50 group-hover:text-white/80 transition-colors duration-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15L12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9" />
          </svg>
        </button>
      </div>

      <div ref="outputSection" :class="['flex-col w-full h-full lg:shrink gap-3 overflow-hidden', hasStartedTransform ? 'flex' : 'hidden lg:flex']">
        <div :class="['relative glass-card backdrop-blur-[25px] p-4 items-center justify-center h-[38vh] md:h-[600px] lg:h-full lg:flex-grow lg:min-h-0 transform-gpu backface-hidden',
          !hasStartedTransform ? 'max-lg:hidden' : '']">
          
          <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center z-30 rounded-2xl">
            <img src="@/assets/svg/staff_logo.svg" class="wave-animation h-32 w-32 md:h-48 md:w-48 opacity-40" />
          </div>

          <div v-else-if="outputImageUrl" @click="modalStore.openOutput()" class="relative w-full h-full flex items-center justify-center cursor-pointer group/output" title="Click to view full screen">
            <img :src="outputImageUrl" alt="Output" class="max-w-full max-h-full rounded-2xl transition-opacity duration-500" :style="{ opacity: outputImageLoaded ? 1 : 0 }" @load="onOutputImageLoad" />
          </div>

          <div v-else class="flex flex-col items-center justify-center space-y-4">
            <svg class="w-16 h-16 md:w-24 md:h-24 text-white/30" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
            </svg>
            <p class="text-base lg:text-xl font-medium text-white/70">{{ $t('workspace.final_result') }}</p>
          </div>
        </div>

        <div class="hidden lg:flex shrink-0">
          <button
            @click="handleButtonClick"
            :disabled="isButtonDisabled"
            :class="[
              'w-full bg-[#3a3a3a] border border-white/[0.02] rounded-2xl min-h-[80px] py-6 text-center text-2xl font-bold text-white cursor-pointer transition-all duration-300 relative overflow-hidden shadow-xl',
              isButtonDisabled ? 'cursor-not-allowed' : 'hover:bg-[#454545]'
            ]"
          >
            <div v-if="!isLoading" class="absolute inset-0 w-full h-full shimmer-effect pointer-events-none"></div>
            <span class="relative z-10" :class="{ 'text-shimmer inline-block': isLoading }">{{ buttonText }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="hasStartedTransform" class="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-md h-28 bg-gradient-to-t from-[#1c1c1c] via-[#1c1c1c]/80 to-transparent z-40 pointer-events-none lg:hidden"></div>

    <div :class="['lg:hidden shrink-0', !hasStartedTransform ? 'static bg-none px-[1px]' : 'fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-md z-50 px-[17px] pb-[13px] pt-4']">
      <button 
        @click="handleButtonClick"
        :disabled="isButtonDisabled"
        :class="[
          'w-full bg-[#3a3a3a] border border-white/[0.02] rounded-2xl min-h-[58px] py-4 text-center text-base font-bold text-white cursor-pointer transition-all duration-300 relative overflow-hidden shadow-xl',
          isButtonDisabled ? 'cursor-not-allowed' : 'hover:bg-[#454545]'
        ]"
      >
        <div v-if="!isLoading" class="absolute inset-0 w-full h-full shimmer-effect pointer-events-none"></div>
        <span class="relative z-10" :class="{ 'text-shimmer inline-block': isLoading }">{{ buttonText }}</span>
      </button>
    </div>

    <transition 
      enter-active-class="transition duration-500 ease-out" 
      enter-from-class="opacity-0" 
      enter-to-class="opacity-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="modalStore.isTipsOpen" class="fixed inset-0 flex items-center justify-center z-[100] bg-black/60 backdrop-blur-xl" @click.self="modalStore.closeTips()">
        <div class="solid-panel w-11/12 max-w-lg relative overflow-hidden h-auto max-h-[94vh] flex flex-col">
          <div 
            ref="scrollContainer"
            @scroll="checkScroll"
            class="no-scrollbar mask-fade-vertical flex-1 min-h-0 overflow-y-auto"
            :style="{
              '--mask-top': canScrollUp ? '60px' : '0px',
              '--mask-bottom': canScrollDown ? '60px' : '0px'
            }"
          >
            <div class="pt-8 pb-6 px-4 md:px-8 flex flex-col gap-8 text-gray-200">
              <div class="text-center relative z-10">

                <h3 class="text-[18px] font-semibold text-white tracking-tight leading-tight mx-auto px-4 w-full text-center">{{ $t('workspace.photo_tips_title') || 'Поради щодо фото' }}</h3>
              </div>

              <div class="space-y-4 px-2 relative z-10 text-left">
                <div class="flex gap-4 items-center group">
                  <div class="shrink-0">
                    <div class="w-1.5 h-1.5 rounded-full bg-white/40 group-hover:bg-white group-hover:scale-125 transition-all"></div>
                  </div>
                  <div class="flex-1">
                    <p class="text-white/70 text-sm md:text-base leading-relaxed group-hover:text-white transition-colors">
                      <span class="font-semibold text-white">{{ $t('workspace.tip_1_title') }}</span> 
                      {{ $t('workspace.tip_1_desc') }}
                    </p>
                  </div>
                </div>

                <div class="flex gap-4 items-center group">
                  <div class="shrink-0">
                    <div class="w-1.5 h-1.5 rounded-full bg-white/40 group-hover:bg-white group-hover:scale-125 transition-all"></div>
                  </div>
                  <div class="flex-1">
                    <p class="text-white/70 text-sm md:text-base leading-relaxed group-hover:text-white transition-colors">
                      <span class="font-semibold text-white">{{ $t('workspace.tip_2_title') }}</span> 
                      {{ $t('workspace.tip_2_desc') }}
                    </p>
                  </div>
                </div>

                <div class="flex gap-4 items-center group">
                  <div class="shrink-0">
                    <div class="w-1.5 h-1.5 rounded-full bg-white/40 group-hover:bg-white group-hover:scale-125 transition-all"></div>
                  </div>
                  <div class="flex-1">
                    <p class="text-white/70 text-sm md:text-base leading-relaxed group-hover:text-white transition-colors">
                      <span class="font-semibold text-white">{{ $t('workspace.tip_3_title') }}</span> 
                      {{ $t('workspace.tip_3_desc') }}
                    </p>
                  </div>
                </div>

                <div class="flex gap-4 items-center group">
                  <div class="shrink-0">
                    <div class="w-1.5 h-1.5 rounded-full bg-white/40 group-hover:bg-white group-hover:scale-125 transition-all"></div>
                  </div>
                  <div class="flex-1">
                    <p class="text-white/70 text-sm md:text-base leading-relaxed group-hover:text-white transition-colors">
                      <span class="font-semibold text-white">{{ $t('workspace.tip_4_title') }}</span> 
                      {{ $t('workspace.tip_4_desc') }}
                    </p>
                  </div>
                </div>

                <div class="flex gap-4 items-center group">
                  <div class="shrink-0">
                    <div class="w-1.5 h-1.5 rounded-full bg-white/40 group-hover:bg-white group-hover:scale-125 transition-all"></div>
                  </div>
                  <div class="flex-1">
                    <p class="text-white/70 text-sm md:text-base leading-relaxed group-hover:text-white transition-colors">
                      <span class="font-semibold text-white">{{ $t('workspace.tip_5_title') }}</span> 
                      {{ $t('workspace.tip_5_desc') }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="px-6 pb-7 pt-2 shrink-0 z-20">
            <button 
              @click="modalStore.closeTips()"
              class="w-full bg-white/[0.08] hover:bg-white/[0.12] active:scale-[0.98] transition-all text-white font-bold rounded-xl py-3.5 text-[15px]"
            >
              {{ $t('workspace.got_it') }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <transition 
      enter-active-class="transition duration-500 ease-out" 
      enter-from-class="opacity-0" 
      enter-to-class="opacity-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="modalStore.isOutputOpen" class="fixed inset-0 flex items-center justify-center z-[120] bg-black/60 backdrop-blur-xl p-4" @click="modalStore.closeOutput()">
        <div class="relative w-full h-full max-w-lg flex flex-col items-center justify-center gap-6 pointer-events-none">
             <div class="relative flex-1 min-h-0 w-full flex items-center justify-center">
               <img :src="outputImageUrl" class="max-w-full max-h-full object-contain pointer-events-auto shadow-2xl rounded-2xl" />
             </div>
             
             <div class="shrink-0 flex items-center gap-4 pointer-events-auto w-full px-4">
               <button @click.stop="downloadOutputImage" class="flex-1 glass-card !flex-row !shadow-none !p-0 h-12 items-center justify-center gap-2 hover:bg-white/10 active:scale-[0.98] transition-all rounded-xl">
                 <svg class="w-5 h-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                   <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                 </svg>
                 <span class="text-white font-medium">{{ $t('workspace.download') || 'Save' }}</span>
               </button>

               <button @click.stop="shareImage" class="flex-1 glass-card !flex-row !shadow-none !p-0 h-12 items-center justify-center gap-2 hover:bg-white/10 active:scale-[0.98] transition-all rounded-xl">
                 <svg class="w-5 h-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                   <path stroke-linecap="round" stroke-linejoin="round" d="M7.217 10.907a2.25 2.25 0 100 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186l9.566-5.314m-9.566 7.5l9.566 5.314m0 0a2.25 2.25 0 103.935 2.186 2.25 2.25 0 00-3.935-2.186zm0-12.814a2.25 2.25 0 103.933-2.185 2.25 2.25 0 00-3.933 2.185z" />
                 </svg>
                 <span class="text-white font-medium">{{ $t('workspace.share') || 'Share' }}</span>
               </button>
             </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, computed, nextTick, onUnmounted } from 'vue';
import api from '@/services/api';
import { useModalStore } from '@/stores/modal';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const modalStore = useModalStore();
const scrollContainer = ref(null);
const canScrollUp = ref(false);
const canScrollDown = ref(false);

function checkScroll() {
  const el = scrollContainer.value;
  if (!el) return;
  canScrollUp.value = el.scrollTop > 10;
  canScrollDown.value = el.scrollTop + el.clientHeight < el.scrollHeight - 10;
}

watch(() => modalStore.isTipsOpen, (newVal) => {
  if (newVal) {
    nextTick(checkScroll);
  }
});

async function urlToFile(url, filename) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Failed to fetch image from URL: ${response.statusText}`);
    }
    const blob = await response.blob();
    return new File([blob], filename, { type: blob.type || 'image/jpeg' });
}

const props = defineProps({
  selectedStyleName: {
    type: String,
    required: false,
    default: null,
  },
  selectedStyleId: {
    type: [Number, String],
    required: false,
    default: null,
  },
  onOpenStylePanel: {
    type: Function,
    required: true,
  },
  latestGenerationData: {
    type: Object,
    default: null,
  }
});

const inputImageUrl = ref(null);
const inputImageFile = ref(null);
const outputImageUrl = ref(null);
const isLoading = ref(false);
const hasStartedTransform = ref(false);
const fileInput = ref(null);
const currentGenerationId = ref(null);
const inputImageLoaded = ref(false);
const outputImageLoaded = ref(false);
const completedGenerationId = ref(null);

const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_FILE_SIZE_BYTES = 7 * 1024 * 1024;
const POLL_INTERVALS_MS = [
  5000, 5000, 5000, 5000, 5000, 5000,
  5000, 5000, 5000
];

let pollingTimeoutId = null;
let cancellationTimeoutId = null;
let deletionTimeoutId = null;
let pollAttempt = 0;

watch(() => props.latestGenerationData, (latest) => {
  if (deletionTimeoutId) {
    clearTimeout(deletionTimeoutId);
    deletionTimeoutId = null;
  }

  if (latest && latest.status === 'processing') {
    isLoading.value = true;
    currentGenerationId.value = latest.id;
    inputImageUrl.value = null;
    outputImageUrl.value = null;
    startPolling(latest.created_at);
  }
  if (latest && !latest.is_visible) {
    const createdAt = new Date(latest.created_at).getTime();
    const age = Date.now() - createdAt;
    const fiveMinutes = 5 * 60 * 1000;

    if (age > fiveMinutes) {
      deleteLongRunningRequest(latest.id);
    } 
    else {
      const remainingTime = fiveMinutes - age;
      deletionTimeoutId = setTimeout(() => {
        deleteLongRunningRequest(latest.id);
      }, remainingTime);
    }
  }
}, { immediate: true });

watch(inputImageUrl, (newVal) => {
  
  if (!newVal) {
    inputImageFile.value = null;
    inputImageLoaded.value = false;
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
  else {
    inputImageLoaded.value = false;
  }
});

watch(outputImageUrl, (newVal, oldVal) => {
  if (oldVal && oldVal.startsWith('blob:')) {
    URL.revokeObjectURL(oldVal);
  }
  if (newVal) {
    outputImageLoaded.value = false;
  }
});

function stopPolling() {
  if (pollingTimeoutId) {
    clearTimeout(pollingTimeoutId);
    pollingTimeoutId = null;
  }
  if (cancellationTimeoutId) {
    clearTimeout(cancellationTimeoutId);
    cancellationTimeoutId = null;
  }
  if (deletionTimeoutId) {
    clearTimeout(deletionTimeoutId);
    deletionTimeoutId = null;
  }
}

async function deleteLongRunningRequest(id) {
  try {
    const finalCheckResponse = await api.get('/api/generations/generation-requests/latest/');
    const finalCheckLatest = finalCheckResponse.data;

    if (finalCheckLatest && finalCheckLatest.id === id) {
      if (!finalCheckLatest.is_visible) {
        await api.delete(`/api/generations/generation-requests/delete/${id}/`);
        modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_timeout') });
      } 
      else if (finalCheckLatest.status === 'completed' && finalCheckLatest.output_large_signed_url) {
        outputImageUrl.value = finalCheckLatest.output_large_signed_url;
        completedGenerationId.value = finalCheckLatest.id;
      }
    }
  }
  catch (err) {
    modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_cancel_failed') });
  }
  finally {
    isLoading.value = false;
    stopPolling();
    currentGenerationId.value = null;
  }
}

async function pollForResult() {
  if (pollAttempt >= POLL_INTERVALS_MS.length) {
    return;
  }

  try {
    const response = await api.get('/api/generations/generation-requests/latest/');
    const latest = response.data;

    if (latest && !latest.is_visible) {
      const nextInterval = POLL_INTERVALS_MS[pollAttempt];
      pollAttempt++;
      pollingTimeoutId = setTimeout(pollForResult, nextInterval);
      return;
    }

    if (latest?.status === 'completed' && latest.output_large_signed_url) {
      try {
        const res = await fetch(latest.output_large_signed_url);
        if (res.ok) {
          const blob = await res.blob();
          outputImageUrl.value = URL.createObjectURL(blob);
        }
        else {
      outputImageUrl.value = latest.output_large_signed_url;
        }
      }
      catch (e) {
        outputImageUrl.value = latest.output_large_signed_url;
      }
      
      completedGenerationId.value = latest.id;
      isLoading.value = false;
      stopPolling();
      currentGenerationId.value = null;
      modalStore.openOutput();
    }
    else if (latest?.status === 'failed') {
      modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_failed_spell') });
      isLoading.value = false;
      stopPolling();
      currentGenerationId.value = null;
    }
    else if (latest?.status === 'rejected_by_safety') {
        modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_safety_rejected') });
        inputImageUrl.value = null;
        outputImageUrl.value = null;
        isLoading.value = false;
        hasStartedTransform.value = false;
        stopPolling();
        currentGenerationId.value = null;
    }
    else {
      const nextInterval = POLL_INTERVALS_MS[pollAttempt];
      pollAttempt++;
      pollingTimeoutId = setTimeout(pollForResult, nextInterval);
    }
  }
  catch (err) {
    modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_status_check') });
    isLoading.value = false;
    stopPolling();
    currentGenerationId.value = null;
  }
}

function startPolling(createdAt = null) {
  stopPolling();
  pollAttempt = 0;
  pollForResult();

  const fiveMinutesInMs = 5 * 60 * 1000;
  let timeoutDuration = fiveMinutesInMs;

  if (createdAt) {
    const startTime = new Date(createdAt).getTime();
    const elapsedTime = Date.now() - startTime;
    timeoutDuration = Math.max(0, fiveMinutesInMs - elapsedTime);
  }

  cancellationTimeoutId = setTimeout(() => {
    if (isLoading.value && currentGenerationId.value) {
      deleteLongRunningRequest(currentGenerationId.value);
    }
  }, timeoutDuration);
}

onUnmounted(() => {
  stopPolling();
  if (deletionTimeoutId) {
    clearTimeout(deletionTimeoutId);
  }
});

const buttonText = computed(() => {
  if (isLoading.value) return t('workspace.transforming') || 'Transforming...';
  return t('workspace.transform_button') || 'Transform Photo';
});

const isButtonDisabled = computed(() => {
  return isLoading.value;
});

function handleButtonClick() {
  if (!isLoading.value) {
    handleGenerate();
  }
}

async function handleGenerate() {
  if (isLoading.value) return;
  if (!inputImageFile.value && !inputImageUrl.value) {
    triggerFileInput();
    return;
  }
  
  if (!props.selectedStyleId) {
    return;
  }
  hasStartedTransform.value = true;
  isLoading.value = true;

  if (window.innerWidth < 1024) {
    nextTick(() => {
      window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: 'smooth'
      });
    });
  }

  outputImageUrl.value = null;
  completedGenerationId.value = null;

  try {
    let fileToUpload = inputImageFile.value;
    if (!fileToUpload && inputImageUrl.value) {
      fileToUpload = await urlToFile(inputImageUrl.value, 'reloaded-image.jpeg');
    }

    const formData = new FormData();
    formData.append('chosen_style', props.selectedStyleId);
    formData.append('input_image', fileToUpload);

    const response = await api.post('/api/generations/generation-requests/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    if (response.data && response.data.id) {
      currentGenerationId.value = response.data.id;
    }

    startPolling();
  }
  catch (err) {
    isLoading.value = false;
    const detail = err.response?.data?.detail || '';
    if (detail.includes('generations')) {
      modalStore.openStore();
    }
    else {
      modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_create_request') });
    }
  }
}

function triggerFileInput() {
  fileInput.value?.click();
}

function onFileSelected(event) {
  const target = event.target;
  const file = target.files?.[0];
  handleFile(file);
}

function handleFile(file) {
  if (!file) {
    return;
  }

  outputImageUrl.value = null;
  inputImageLoaded.value = false;
  hasStartedTransform.value = false;

  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_invalid_type') });
    return;
  }
  else if (file.size > MAX_FILE_SIZE_BYTES) {
    modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_file_size') });
    return;
  }

  inputImageFile.value = file;
  const reader = new FileReader();
  reader.onload = (event) => {
    inputImageUrl.value = event.target?.result;
  };
  reader.readAsDataURL(file);
}

function onInputImageLoad() {
  inputImageLoaded.value = true;
}

function onOutputImageLoad() {
  outputImageLoaded.value = true;
}

async function downloadOutputImage() {
  if (!completedGenerationId.value) {
    modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_download') });
    return;
  }

  try {
    const response = await api.get(`api/generations/generation-requests/download/${completedGenerationId.value}/`);
    const link = document.createElement('a');
    link.href = response.data.download_url;
    link.setAttribute('download', `ervelus-image-${completedGenerationId.value}.png`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  catch (err) {
    modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_download') });
  }
}

async function shareImage() {
  if (!completedGenerationId.value) return;

  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.switchInlineQuery(`share_${completedGenerationId.value}`, ['users', 'groups', 'channels']);
  } 
  else {
    modalStore.openModal({ title: t('workspace.share'), message: t('workspace.share_not_supported') });
  }
}
</script>

<style scoped>
@keyframes shimmer-text {
  0% { background-position: 200% center; }
  100% { background-position: -200% center; }
}

@keyframes shimmer-slide {
  0% { transform: translateX(-150%) skewX(-20deg); }
  100% { transform: translateX(150%) skewX(-20deg); }
}

@keyframes wave-pulse {
  0%, 100% { transform: rotate(35deg); opacity: 0.4; }
  25% { transform: rotate(50deg); }
  50% { opacity: 0.6; }
  75% { transform: rotate(40deg); }
}

.text-shimmer {
  background: linear-gradient(
    90deg, 
    rgba(255,255,255,1) 0%, 
    rgba(255,255,255,0.3) 25%, 
    rgba(255,255,255,1) 50%, 
    rgba(255,255,255,0.3) 75%, 
    rgba(255,255,255,1) 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer-text 4s linear infinite;
}

.shimmer-effect {
  background: linear-gradient(
    to right,
    transparent 0%,
    rgba(255, 255, 255, 0) 30%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 70%,
    transparent 100%
  );
  animation: shimmer-slide 3s infinite;
  filter: blur(5px);
}

.wave-animation {
  animation: wave-pulse 2.5s ease-in-out infinite;
}

.mask-fade-vertical {
  mask-image: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0,0,0,0.4) calc(var(--mask-top, 0px) / 2),
    black var(--mask-top, 0px),
    black calc(100% - var(--mask-bottom, 0px)),
    rgba(0,0,0,0.4) calc(100% - (var(--mask-bottom, 0px) / 2)),
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0,0,0,0.4) calc(var(--mask-top, 0px) / 2),
    black var(--mask-top, 0px),
    black calc(100% - var(--mask-bottom, 0px)),
    rgba(0,0,0,0.4) calc(100% - (var(--mask-bottom, 0px) / 2)),
    transparent 100%
  );
  transition: mask-image 0.3s ease-in-out, -webkit-mask-image 0.3s ease-in-out;
}
</style>