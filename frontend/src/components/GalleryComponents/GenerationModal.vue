<template>
  <Transition name="modal">
    <div v-if="isOpen" class="relative z-50">
      <div class="fixed inset-0 modal-overlay transition-opacity" />

      <div class="fixed inset-0 z-50 overflow-y-auto" @click="emit('close-modal')">
        <div class="flex min-h-full items-center justify-center p-3 text-center">
          <Transition name="fade-content">
            <div v-if="isLoading && isMobile" key="spinner" class="spinner"></div>

            <div
              v-else
              :class="[
                'relative flex w-full max-w-[1400px] md:h-[90vh] transform flex-col overflow-hidden rounded-2xl border border-white/10 bg-zinc-900/50 text-left align-middle shadow-xl backdrop-blur transition-all',
              ]"
            >
              <button @click="emit('close-modal')"
                class="absolute right-0 top-0 p-2 text-white hover:text-white/80 transition-all duration-300 z-50 md:hidden">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              <Transition name="fade-content">
                <div v-if="!isLoading && currentRequest" class="flex h-full flex-col">
                  <div class="flex-grow flex flex-col md:flex-row justify-center items-stretch gap-4 px-6 pt-8 pb-3 min-h-0">
                    <div class="flex-1 flex justify-center items-center min-w-0">
                      <img
                        v-if="currentRequest.input_large_signed_url"
                        :src="currentRequest.input_large_signed_url"
                        alt="Input image"
                        class="block max-w-full max-h-full object-contain rounded-2xl"
                      />
                      <div v-else class="h-44 md:h-full w-full flex items-center justify-center text-zinc-500 text-sm font-medium border border-zinc-800 rounded-2xl md:border-0">
                        Failed to generate input image
                      </div>
                    </div>
                    <div class="flex-1 flex justify-center items-center min-w-0">
                      <img
                        v-if="currentRequest.output_large_signed_url"
                        :src="currentRequest.output_large_signed_url"
                        alt="Output image"
                        class="block max-w-full max-h-full object-contain rounded-2xl"
                      />
                      <div v-else class="h-44 md:h-full w-full flex items-center justify-center text-zinc-500 text-sm font-medium border border-zinc-800 rounded-2xl md:border-0">
                        Failed to generate output image
                      </div>
                    </div>
                  </div>

                  <div class="flex-shrink-0 flex h-20 items-center justify-between px-6 pb-2">
                    <div class="flex items-center justify-between w-full">
                      <div class="text-left">
                        <p class="font-semibold text-zinc-300 truncate" :title="currentStyleName || 'Deleted Style'">
                          {{ currentStyleName || 'Deleted Style' }}
                        </p>
                        <p v-if="currentFormattedDate" class="text-sm text-zinc-400">{{ currentFormattedDate }}</p>
                      </div>
                      <div class="flex items-center gap-x-6">
                        <button
                          type="button"
                          @click.prevent.stop="downloadOutput(currentRequest)"
                          :disabled="!currentRequest.output_large_signed_url"
                          class="h-min w-min inline-flex justify-center text-zinc-400 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          title="Download"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-download w-6 h-6">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                          </svg>
                        </button>
                        <button
                          type="button"
                          @click.stop="$emit('delete-request', currentRequest)"
                          class="h-min w-min inline-flex justify-center text-zinc-400 hover:text-red-400 transition-colors"
                          title="Delete"
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
    </div>
  </Transition>
</template>

<script setup>
import api from '@/services/api'
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { toast } from '@/services/toast';

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
        currentFormattedDate.value = new Date(response.data.created_at).toLocaleString(undefined);
      }
      else {
        currentFormattedDate.value = '';
      }
    }
  }
  catch (error) {
    if (error.response && error.response.status === 404) {
      toast.info(error.response.data.detail || 'Request not found');
    }
    else {
      toast.info('An error occurred while fetching the generation');
    }
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
    const url = response.data?.download_url || '';
    
    const link = document.createElement('a');
    link.href = url;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  catch (error) {
    if (error.response && (error.response.status === 404 || error.response.status === 400)) {
      toast.info(error.response.data.detail || 'Download failed');
    }
    else {
      toast.info('Download failed');
    }
  }
};

watch(() => props.isOpen, (newVal) => {
  if (newVal && props.selectedRequest) {
    getCurrentRequest(props.selectedRequest);
  }
  else {
    currentRequest.value = null;
    currentStyleName.value = '';
    currentFormattedDate.value = '';
  }
});

onMounted(() => {
  handleResize();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize); 
});
</script>

<style scoped>
.modal-enter-active {
  transition: all 300ms ease-out;
}

.modal-enter-active .modal-overlay {
  transition: opacity 300ms ease-out;
}

.modal-enter-active .transform {
  transition: all 300ms ease-out;
}

.modal-enter-from .modal-overlay {
  opacity: 0;
}

.modal-enter-from .transform {
  opacity: 0;
  transform: translateY(4px) scale(0.95);
}

@media (min-width: 640px) {
  .modal-enter-from .transform {
    transform: translateY(0) scale(0.95);
  }
}

.modal-leave-active {
  transition: all 200ms ease-in;
}

.modal-leave-active .modal-overlay {
  transition: opacity 200ms ease-in;
}

.modal-leave-active .transform {
  transition: all 200ms ease-in;
}

.modal-leave-to .modal-overlay {
  opacity: 0;
}

.modal-leave-to .transform {
  opacity: 0;
  transform: translateY(4px) scale(0.95);
}

@media (min-width: 640px) {
  .modal-leave-to .transform {
    transform: translateY(0) scale(0.95);
  }
}

.modal-overlay {
  background-color: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(15px);
}

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