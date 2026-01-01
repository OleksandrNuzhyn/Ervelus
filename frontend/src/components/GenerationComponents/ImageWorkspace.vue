<template>
  <div :class="['flex flex-col px-3 pt-3 gap-3 lg:min-h-[calc(100vh-9rem)] relative overflow-hidden', 
    hasStartedTransform ? 'pb-21 lg:pb-3' : 'pb-3']">
    <div class="flex-grow flex flex-col lg:grid lg:grid-cols-2 gap-3 lg:gap-6 pb-0 overflow-visible">
      <div class="flex flex-col gap-3 lg:shrink overflow-visible">
        <div class="relative w-full lg:flex-grow lg:flex lg:flex-col overflow-visible">
          <div :class="['bg-black/30 backdrop-blur-[7px] shadow-[0_0_1.5px_rgba(0,0,0,0.8)] rounded-xl p-4 flex flex-col items-center justify-center transition-all duration-500 h-[38vh] md:h-[600px] lg:h-auto lg:flex-grow lg:min-h-0 overflow-visible', 
            inputImageUrl ? 'border-gray-600/30' : 'border-transparent']">
            
            <div v-if="!inputImageUrl" @click="triggerFileInput"
                 class="cursor-pointer w-full h-full flex flex-col items-center justify-center relative group/btn">
              
              <div class="mb-4">
                <svg class="w-16 h-16 md:w-24 md:h-24 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
              </div>
              <p class="text-lg text-gray-400">Click to upload image</p>
              <input type="file" ref="fileInput" @change="onFileSelected" class="hidden" accept="image/jpeg, image/png, image/webp" />
            </div>

            <div v-else class="relative w-full h-full">
              <img :src="inputImageUrl" alt="Input" class="absolute inset-0 w-full h-full object-contain rounded-xl transition-opacity duration-500" :style="{ opacity: inputImageLoaded ? 1 : 0 }" @load="onInputImageLoad" />
              <button @click="inputImageUrl = null; outputImageUrl = null; inputImageLoaded = false" 
                class="absolute right-0 top-0 text-white/60 hover:text-white bg-transparent p-2 transition-colors z-20">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <button @click="onOpenStylePanel" class="w-full bg-white/[0.06] backdrop-blur-xl shadow-[0_8px_32px_rgba(0,0,0,0.3)] rounded-xl min-h-[56px] lg:min-h-[80px] py-3.5 lg:py-6 mt-0 flex items-center justify-center relative text-lg md:text-2xl font-semibold cursor-pointer hover:bg-white/[0.12] active:scale-[0.98] transition-all duration-300 text-white px-4 group overflow-visible">
          <div class="flex items-center gap-2">
            <span class="opacity-80 font-medium whitespace-nowrap group-hover:opacity-100 transition-opacity">Style:</span>
            <span class="truncate font-bold">{{ props.selectedStyleName }}</span>
          </div>
          <svg class="absolute right-5 top-[54%] -translate-y-1/2 w-4 h-4 md:w-6 md:h-6 opacity-60 group-hover:opacity-100 group-hover:translate-x-1 transition-all" fill="currentColor" viewBox="0 0 20 20">
            <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
          </svg>
        </button>
      </div>

      <div ref="outputSection" :class="['flex-col w-full h-full lg:shrink gap-3 overflow-hidden', hasStartedTransform ? 'flex' : 'hidden lg:flex']">
        <div :class="['relative bg-black/30 backdrop-blur-[7px] shadow-[0_0_1.5px_rgba(0,0,0,0.8)] rounded-xl p-4 flex flex-col items-center justify-center transition-all duration-500 h-[38vh] md:h-[600px] lg:h-auto lg:flex-grow lg:min-h-0',
          outputImageUrl || isLoading ? 'border-gray-600/30' : 'border-transparent',
          !hasStartedTransform ? 'max-lg:hidden' : '']">
          
          <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center z-30 rounded-xl">
            <img src="@/assets/svg/staff_logo.svg" class="wave-animation h-32 w-32 md:h-48 md:w-48 opacity-40" />
          </div>

          <div v-else-if="outputImageUrl" class="relative w-full h-full">
            <img :src="outputImageUrl" alt="Output" class="absolute inset-0 w-full h-full object-contain rounded-xl transition-opacity duration-500" :style="{ opacity: outputImageLoaded ? 1 : 0 }" @load="onOutputImageLoad" />
            <button @click="downloadOutputImage" 
              class="absolute right-0 top-0 text-white/60 hover:text-white bg-transparent p-2 transition-colors z-20">
              <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
              </svg>
            </button>
          </div>

          <div v-else class="text-center text-gray-400">
             <p>Result will appear here</p>
          </div>
        </div>

        <div class="hidden lg:flex shrink-0">
          <button
            @click="handleButtonClick"
            :disabled="isButtonDisabled"
            :class="[
              'w-full bg-white/15 backdrop-blur-xl rounded-xl min-h-[80px] py-6 text-center text-2xl font-bold text-white cursor-pointer transition-all duration-500 relative overflow-hidden',
              isButtonDisabled
                ? 'opacity-40 cursor-not-allowed'
                : 'hover:bg-white/25 active:scale-[0.98]'
            ]"
          >
            <div v-if="!isButtonDisabled" class="absolute inset-0 w-full h-full shimmer-effect pointer-events-none"></div>
            <span class="relative z-10">{{ buttonText }}</span>
          </button>
        </div>
      </div>
    </div>

    <div :class="['lg:hidden shrink-0 transition-all duration-500', 
      hasStartedTransform ? 'fixed bottom-0 left-0 right-0 z-50 px-7 pb-3 pt-4 bg-gradient-to-t from-black/60 to-transparent' : '']">
      <button 
        @click="handleButtonClick"
        :disabled="isButtonDisabled"
        :class="[
          'w-full bg-white/15 backdrop-blur-xl rounded-xl min-h-[58px] py-4 text-center text-xl font-bold text-white cursor-pointer transition-all duration-500 relative overflow-hidden',
          isButtonDisabled 
            ? 'opacity-40 cursor-not-allowed' 
            : 'hover:bg-white/25 active:scale-[0.98]'
        ]"
      >
        <div v-if="!isButtonDisabled" class="absolute inset-0 w-full h-full shimmer-effect pointer-events-none"></div>
        <span class="relative z-10">{{ buttonText }}</span>
      </button>
    </div>

    <transition name="modal-fade">
      <div v-if="showGenerationsModal" class="fixed inset-0 flex items-center justify-center z-[100] confirm-modal-overlay" @click.self="showGenerationsModal = false">
        <div class="modal-content-card p-10 w-11/12 max-w-md shadow-2xl flex flex-col gap-6 text-gray-200 relative">
          <div class="text-center">
            <h3 class="medieval text-3xl text-gray-100 mb-2">Ready for More?</h3>
            <p class="text-gray-300 text-lg mt-4">
              Get more generations and keep creating!
            </p>
          </div>
          <div class="flex justify-center pt-2">
            <router-link to="/pricing" class="manage-button generations-primary-button">
              Get More
            </router-link>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, computed, nextTick } from 'vue';
import api from '@/services/api';
import { toast } from '@/services/toast';

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
const outputSection = ref(null);
const currentGenerationId = ref(null);
const isDragging = ref(false);
const inputImageLoaded = ref(false);
const outputImageLoaded = ref(false);
const completedGenerationId = ref(null);
const showGenerationsModal = ref(false);

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

watch(outputImageUrl, (newVal) => {
  
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
        toast.info("The generation request was cancelled because it took too long to complete.");
      } 
      else if (finalCheckLatest.status === 'completed' && finalCheckLatest.output_large_signed_url) {
        outputImageUrl.value = finalCheckLatest.output_large_signed_url;
        completedGenerationId.value = finalCheckLatest.id;
      }
    }
  }
  catch (err) {
    if (err.response && [400, 404].includes(err.response.status)) {
      toast.info("Could not cancel the generation request. It might have already been completed or cancelled.");
    }
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
      outputImageUrl.value = latest.output_large_signed_url;
      completedGenerationId.value = latest.id;
      isLoading.value = false;
      stopPolling();
      currentGenerationId.value = null;
    }
    else if (latest?.status === 'failed') {
      toast.info("The spell has failed! Try casting the magic again.");
      isLoading.value = false;
      stopPolling();
      currentGenerationId.value = null;
    }
    else if (latest?.status === 'rejected_by_safety') {
        toast.info("This dark magic was rejected by the safety system. Try another image.");
        inputImageUrl.value = null;
        outputImageUrl.value = null;
        isLoading.value = false;
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
    const errorMessage = err.response?.data?.detail || 'An unexpected error occurred while checking generation status.';
    toast.info(errorMessage);
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

const styleButtonText = computed(() => {
  return props.selectedStyleName || '';
});

const buttonText = computed(() => {
  if (isLoading.value) return 'Transforming...';
  return 'Transform Photo';
});

const isButtonDisabled = computed(() => {
  return isLoading.value;
});

function handleButtonClick() {
  if (!isLoading.value) {
    handleGenerate();
  }
}

function getErrorMessage(err, endpoint) {
  if (!err.response) {
    return null;
  }

  const { status, data } = err.response;
  const serverError = data?.detail;

  if (status === 400) {
    if (endpoint === 'create') {
      return serverError || data?.non_field_errors?.[0] || 'Could not create request. Please try again later.';
    }
    else if (endpoint === 'download') {
      return serverError || 'Could not download the image. Please try again later.';
    }
  }
  else if (status === 404) {
    if (endpoint === 'download') {
      return serverError || 'File for download not found. Please try again later.';
    }
  }
  return null;
}

async function handleGenerate() {
  if (isLoading.value) return;
  if ((!inputImageFile.value && !inputImageUrl.value) || !props.selectedStyleId) {
    toast.info('Choose your photo and style');
    return;
  }
  hasStartedTransform.value = true;
  isLoading.value = true;

  nextTick(() => {
    outputSection.value?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
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
    if (err.response && err.response.status === 400) {
        const message = getErrorMessage(err, 'create');
        if (message && message.includes('generations')) {
            showGenerationsModal.value = true;
        }
        else {
            toast.info(message);
        }
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

  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    toast.info('Invalid file type. Our magicians support only JPEG, PNG or WEBP format.');
    return;
  }
  else if (file.size > MAX_FILE_SIZE_BYTES) {
    toast.info('Maximum file size is 7 MB.');
    return;
  }

  inputImageFile.value = file;
  const reader = new FileReader();
  reader.onload = (event) => {
    inputImageUrl.value = event.target?.result;
  };
  reader.readAsDataURL(file);
}

function onDragEnter(event) {
  event.preventDefault();
  isDragging.value = true;
}

function onDragOver(event) {
  event.preventDefault();
}

function onDragLeave(event) {
  event.preventDefault();
  isDragging.value = false;
}

function onDrop(event) {
  event.preventDefault();
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  handleFile(file);
}

function onInputImageLoad() {
  inputImageLoaded.value = true;
}

function onOutputImageLoad() {
  outputImageLoaded.value = true;
}

async function downloadOutputImage() {
  if (!completedGenerationId.value) {
    toast.info("Cannot download image. Please try again later.");
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
    if (err.response && [400, 404].includes(err.response.status)) {
      toast.info(getErrorMessage(err, 'download'));
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');

@keyframes wave {
  0%, 100% { transform: rotate(35deg)}
  25% { transform: rotate(50deg)}
  75% { transform: rotate(40deg)}
  50% {
    opacity: 0.45;
  }
}

.wave-animation {
  animation: wave 2.5s ease-in-out infinite;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

@media (max-width: 380px) { 
  .modal-text {
    font-size: 1rem;
    line-height: 1.4;
    word-break: break-word;
  }
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-out;
}

.modal-fade-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

.modal-fade-leave-to {
  opacity: 0;
}

.modal-content-card {
  background: rgba(24, 24, 24, 0.5);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
}

.confirm-modal-overlay {
  background-color: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(15px);
}

.manage-button {
  display: inline-block;
  width: auto;
  min-width: 200px;
  text-align: center;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 9999px;
  padding: 1rem 2.5rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #9ca3af;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  cursor: pointer;
}

.generations-primary-button {
  background: #8b5cf6 !important; 
  color: white !important;
  border: none !important;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
}

.generations-primary-button:hover {
  background: #7c3aed !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(139, 92, 246, 0.4);
  color: white !important;
}

.small-manage-button {
  min-width: 0;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.medieval {
  font-family: 'MedievalSharp', cursive;
}

.blur-mask-dock {
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  mask-image: linear-gradient(to top, black 25%, transparent 100%);
  -webkit-mask-image: linear-gradient(to top, black 25%, transparent 100%);
}

@keyframes shimmer {
  0% { transform: translateX(-150%) skewX(-20deg); }
  100% { transform: translateX(150%) skewX(-20deg); }
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
  animation: shimmer 3s infinite;
  filter: blur(5px);
}
</style>