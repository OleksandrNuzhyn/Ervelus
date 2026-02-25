<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="modalStore.isGalleryOpen" class="fixed inset-0 z-[100] overflow-y-auto bg-black/60 backdrop-blur-[15px]" @click="modalStore.closeGallery()">
        <div class="flex min-h-full items-center justify-center py-6 text-center">
            <Transition name="fade-content">
              <div v-if="isLoading && isMobile" key="spinner" class="spinner"></div>

              <div
                v-else
                :class="[
                  'solid-panel w-11/12 max-w-[1400px] md:h-[90vh] text-left align-middle transition-all overflow-hidden',
                ]"
              >
                <Transition name="fade-content">
                  <div v-if="!isLoading && currentRequest" class="flex h-full flex-col">
                    <div class="flex-grow flex flex-col md:flex-row justify-center items-stretch gap-4 px-6 pt-15 pb-3 min-h-0">
                      <div class="flex-1 flex justify-center items-center min-w-0">
                        <img
                          v-if="currentRequest.input_large_signed_url"
                          :src="currentRequest.input_large_signed_url"
                          alt="Input image"
                          class="block max-w-full max-h-full object-contain rounded-2xl"
                        />
                        <div v-else class="h-44 md:h-full w-full flex items-center justify-center text-zinc-500 text-sm font-medium border border-white/[0.02] rounded-2xl md:border-0">
                          {{ $t('gallery.failed_input') }}
                        </div>
                      </div>
                      <div class="flex-1 flex justify-center items-center min-w-0">
                        <img
                          v-if="currentRequest.output_large_signed_url"
                          :src="currentRequest.output_large_signed_url"
                          alt="Output image"
                          class="block max-w-full max-h-full object-contain rounded-2xl"
                        />
                        <div v-else class="relative w-full flex items-center justify-center">
                          <template v-if="currentRequest.input_large_signed_url">
                             <img :src="currentRequest.input_large_signed_url" class="invisible block max-w-full max-h-full object-contain rounded-2xl" aria-hidden="true" />
                             <div class="absolute inset-0 flex flex-col items-center justify-center gap-3 text-zinc-500 text-sm font-medium border border-white/5 rounded-2xl bg-white/[0.02] backdrop-blur-sm">
                                <svg class="w-14 h-12 text-white/20" fill="none" viewBox="0 0 24 24" stroke="currentColor" preserveAspectRatio="none">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                <span class="text-white/40 text-xs">{{ $t('gallery.failed_output') }}</span>
                             </div>
                          </template>
                          <div v-else class="h-44 md:h-full w-full flex flex-col items-center justify-center gap-3 text-zinc-500 text-sm font-medium border border-white/5 rounded-2xl bg-white/[0.02] md:border-0">
                                <svg class="w-14 h-12 text-white/20" fill="none" viewBox="0 0 24 24" stroke="currentColor" preserveAspectRatio="none">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                <span class="text-white/40 text-xs">{{ $t('gallery.failed_output') }}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="flex-shrink-0 flex h-20 items-center justify-between px-6 pb-2">
                      <div class="flex items-center justify-between w-full">
                        <div class="text-left">
                          <p class="font-semibold text-zinc-300 truncate" :title="currentStyleName || $t('gallery.deleted_style')">
                            {{ currentStyleName || $t('gallery.deleted_style') }}
                          </p>
                          <p v-if="currentFormattedDate" class="text-sm text-zinc-400">{{ currentFormattedDate }}</p>
                        </div>
                        <div class="flex items-center gap-x-6">
                          <button
                            type="button"
                            @click.prevent.stop="shareImage(currentRequest)"
                            class="h-min w-min inline-flex justify-center text-zinc-400 hover:text-[#2AABEE] transition-colors"
                            :title="$t('gallery.share')"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="5 5 22 22" fill="currentColor" class="w-7 h-7">
                              <path d="M22.9866 10.2088C23.1112 9.40332 22.3454 8.76755 21.6292 9.082L7.36482 15.3448C6.85123 15.5703 6.8888 16.3483 7.42147 16.5179L10.3631 17.4547C10.9246 17.6335 11.5325 17.541 12.0228 17.2023L18.655 12.6203C18.855 12.4821 19.073 12.7665 18.9021 12.9426L14.1281 17.8646C13.665 18.3421 13.7569 19.1512 14.314 19.5005L19.659 22.8523C20.2585 23.2282 21.0297 22.8506 21.1418 22.1261L22.9866 10.2088Z"/>
                            </svg>
                          </button>
                          <button
                            type="button"
                            @click.prevent.stop="downloadOutput(currentRequest)"
                            :disabled="!currentRequest.output_large_signed_url"
                            class="h-min w-min inline-flex justify-center text-zinc-400 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            :title="$t('gallery.download')"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                            </svg>
                          </button>
                          <button
                            type="button"
                            @click.stop="$emit('delete-request', currentRequest)"
                            class="h-min w-min inline-flex justify-center text-zinc-400 hover:text-red-400 transition-colors"
                            :title="$t('gallery.delete')"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2 w-6 h-6">
                              <polyline points="3 6 5 6 21 6"></polyline>
                              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                              <line x1="10" y1="11" x2="10" y2="17"></line>
                              <line x1="14" y1="11" x2="14" y2="17"></line>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </Transition>

                <div v-if="isLoading && !isMobile" class="absolute inset-0 z-10 flex items-center justify-center">
                    <div :class="{'unified-shimmer-container': !isMobile}" class="h-full w-full">
                    <div class="stars-loader"></div>
                  </div>
                </div>
              </div>
            </Transition>
          </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import api from '@/services/api'
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();

const props = defineProps({
  isOpen: { type: Boolean, required: true },
  selectedRequest: { type: Object, default: null }
});

const emit = defineEmits(['close-modal', 'delete-request']);

const currentRequest = ref(null);
const currentStyleName = ref('');
const currentFormattedDate = ref('');
const isLoading = ref(false);
const isMobile = ref(false);
const modalStore = useModalStore();

function handleResize() {
  isMobile.value = window.innerWidth < 768;
}

async function preloadRequest(urlsToLoad) {
  const promises = urlsToLoad.map(urlToLoad => {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = resolve
      img.onerror = reject
      img.src = urlToLoad
    })
  })
  await Promise.all(promises)
}

async function getCurrentRequest(request) {
  isLoading.value = true;
  
  try {
    const response = await api.get(`/api/generations/generation-requests/retrieve/${request.id}/`);

    const urlsToLoad = [response.data?.input_large_signed_url, response.data?.output_large_signed_url].filter(Boolean);
    if (urlsToLoad.length > 0) {
      await preloadRequest(urlsToLoad);
    }
    
    if (props.isOpen && props.selectedRequest.id === request.id) {
      currentRequest.value = response.data;
      currentStyleName.value = response.data?.chosen_style_name || '';
      
      if (response.data?.created_at) {
        currentFormattedDate.value = new Date(response.data.created_at).toLocaleString(locale.value);
      }
      else {
        currentFormattedDate.value = '';
      }
    }
  }
  catch (error) {
    modalStore.openModal({ title: t('gallery.delete_title'), message: t('gallery.error_fetch') });
    emit('close-modal');
  }
  finally {
    if (props.isOpen && props.selectedRequest.id === request.id) {
      isLoading.value = false;
    }
  }
}

async function downloadOutput(request) {
  try {
    const response = await api.get(`/api/generations/generation-requests/download/${request.id}/`);
    const { download_url, filename } = response.data;
    
    if (window.Telegram?.WebApp?.downloadFile) {
      window.Telegram.WebApp.downloadFile({ url: download_url, file_name: filename });
    }
  }
  catch (error) {
    modalStore.openModal({ title: t('gallery.delete_title'), message: t('gallery.error_download_failed') });
  }
};

async function shareImage(request) {
  if (!request || !request.id) return;

  if (window.Telegram?.WebApp?.shareMessage) {
    try {
      const response = await api.post(`/api/telegram/prepare-share/${request.id}/`);
      const { prepared_id } = response.data;
      window.Telegram.WebApp.shareMessage(prepared_id);
    }
    catch (err) { 
      modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_create_request') });
    }
  } 
  else if (window.Telegram?.WebApp?.switchInlineQuery) {
    window.Telegram.WebApp.switchInlineQuery(`${request.id}`, ['users', 'groups', 'channels']);
  }
  else {
    modalStore.openModal({ title: t('gallery.share'), message: t('workspace.share_not_supported') });
  }
}

watch([() => modalStore.isGalleryOpen, () => props.selectedRequest], ([isOpen, request]) => {
  if (isOpen && request) {
    getCurrentRequest(request);
  }
  else if (!isOpen) {
    currentRequest.value = null;
    currentStyleName.value = '';
    currentFormattedDate.value = '';
  }
}, { immediate: true });

onMounted(() => {
  handleResize();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize); 
});
</script>

<style scoped>
.fade-content-enter-active {
  transition: opacity 0.7s ease-in-out;
  transform: translateZ(0);
  will-change: opacity, transform;
}

.fade-content-leave-active {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-top: -28px;
  margin-left: -28px;
  animation: fadeOut 0.4s linear;
  transform: translateZ(0);
  will-change: opacity, transform;
}

.fade-content-enter-from,
.fade-content-leave-to {
  opacity: 0;
  transform: translateZ(0);
  will-change: opacity, transform;
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

.spinner {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-left-color: #fff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>