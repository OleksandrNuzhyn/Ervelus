<template>
  <div class="mt-0 p-3 lg:flex lg:flex-col lg:min-h-[calc(100vh-9rem)]">
    <div class="flex flex-col lg:grid lg:grid-cols-2 gap-8 items-start lg:items-stretch lg:flex-grow">
      <div class="z-9 flex flex-col items-center w-full">
        <div class="bg-black/30 backdrop-blur-[7px] shadow-[0_0_3px_rgba(0,0,0)] rounded-lg p-4 h-[400px] md:h-[660px] w-full flex flex-col items-center justify-center lg:h-auto lg:flex-grow lg:min-h-0">
          <div v-if="!inputImageUrl" @click="triggerFileInput"
               @dragenter.prevent="onDragEnter"
               @dragover.prevent="onDragOver"
               @dragleave.prevent="onDragLeave"
               @drop.prevent="onDrop"
               :class="['cursor-pointer w-full h-full flex flex-col items-center justify-center', { 'bg-black/20 border-2 border-dashed border-gray-400': isDragging }]">
            <svg class="w-16 h-16 md:w-24 md:h-24 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
            </svg>
            <p class="mt-4 text-lg text-gray-400">Click here to upload image</p>
            <input type="file" ref="fileInput" @change="onFileSelected" class="hidden" accept="image/jpeg, image/png, image/webp" />
          </div>
          <div v-else class="relative w-full h-full">
            <img 
              :src="inputImageUrl" 
              alt="Input" 
              class="absolute inset-0 w-full h-full object-contain rounded-lg transition-opacity duration-500 ease-in-out"
              :style="{ opacity: inputImageLoaded ? 1 : 0 }"
              @load="onInputImageLoad"
            />
            <button @click="inputImageUrl = null; outputImageUrl = null; inputImageLoaded = false" class="absolute top-1 right-1 bg-gray-800/80 hover:bg-gray-700/90 text-gray-300 hover:text-white p-1.5 transition-colors rounded border border-gray-600/50 hover:border-gray-500">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            </button>
          </div>
        </div>
        <div @click="onOpenStylePanel" class="w-full bg-black/30 backdrop-blur-[7px] shadow-[0_0_3px_rgba(0,0,0)] rounded-xl py-3 lg:py-6 mt-7 lg:mt-4 text-center text-xl md:text-2xl font-bold cursor-pointer hover:bg-black/40 transition-all duration-200 border border-transparent hover:border-gray-600">
          {{ selectedStyleName || 'Choose style' }}
        </div>
      </div>

      <div class="flex flex-col w-full">
        <div class="flex flex-col items-center justify-center bg-black/30 backdrop-blur-[7px] shadow-[0_0_3px_rgba(0,0,0)] rounded-lg p-4 h-[400px] md:h-[660px] lg:h-auto lg:flex-grow lg:min-h-0">
          <div v-if="isLoading" class="flex flex-col items-center justify-center">
            <img src="@/assets/svg/staff_logo.svg" class="wave-animation animation-pulse h-45 w-45 pointer-events-none select-none" />
            <p class="text-gray-400 text-lg">Generating...</p>
          </div>
          <div v-else-if="outputImageUrl" class="relative w-full h-full">
            <img 
              :src="outputImageUrl" 
              alt="Output" 
              class="absolute inset-0 w-full h-full object-contain rounded-lg transition-opacity duration-500 ease-in-out"
              :style="{ opacity: outputImageLoaded ? 1 : 0 }"
              @load="onOutputImageLoad"
            />
            <button @click="downloadOutputImage" class="absolute top-1 right-1 bg-gray-800/80 hover:bg-gray-700/90 text-gray-300 hover:text-white p-1.5 transition-colors rounded border border-gray-600/50 hover:border-gray-500">
                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                </svg>
            </button>
          </div>
          <div v-else class="text-center text-gray-400">
            <p>The result of the generation will appear here</p>
          </div>
        </div>
        <div class="mt-7 lg:mt-4 flex flex-col sm:flex-row justify-center sm:justify-between items-center gap-8 sm:gap-5 md:gap-6 lg:gap-10">
          <button 
            @click="handleButtonClick"
            :disabled="isButtonDisabled"
            :class="[
              'w-full bg-gray-700/50 backdrop-blur-[10px] shadow-[0_0_3px_rgba(0,0,0)] rounded-xl py-3 lg:py-6 text-center text-xl md:text-2xl font-bold text-white cursor-pointer hover:bg-gray-700/40 transition-all duration-200 border border-transparent hover:border-gray-600',
              isButtonDisabled ? 'opacity-60 cursor-not-allowed' : ''
            ]"
          >
            {{ buttonText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, onUnmounted, computed } from 'vue';
import api from '@/services/api';
import { toast } from '@/services/toast';

const urlToFile = async (url, filename) => {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Failed to fetch image from URL: ${response.statusText}`);
    }
    const blob = await response.blob();
    return new File([blob], filename, { type: blob.type || 'image/jpeg' });
};

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
const fileInput = ref(null);
const currentGenerationId = ref(null);
const isStoppingAllowed = ref(false);
const isDragging = ref(false);
const inputImageLoaded = ref(false);
const outputImageLoaded = ref(false);
const completedGenerationId = ref(null);
const isFirstCheck = ref(true);

const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_FILE_SIZE_BYTES = 7 * 1024 * 1024;
const POLL_INTERVALS_MS = [
  5000, 5000, 5000, 5000, 5000, 5000,
  5000, 5000, 5000
];

let stopEnableTimerId = null;
let pollingTimeoutId = null;
let pollAttempt = 0;

watch(() => props.latestGenerationData, (latest) => {
  if (latest) {
    const statuses = ['completed', 'failed', 'stopped_by_user', 'rejected_by_safety'];
    if (isFirstCheck.value && statuses.includes(latest.status)) {
      isFirstCheck.value = false;
      return;
    }
    isFirstCheck.value = false;
    
    if (latest.status === 'processing') {
      isLoading.value = true;
      currentGenerationId.value = latest.id;
      inputImageUrl.value = latest.input_img_signed_url;
      outputImageUrl.value = null;
      startStopEnableTimer(latest.created_at);
      startPolling();
    } 
    else if (latest.status === 'completed' && latest.output_img_signed_url) {
      inputImageUrl.value = latest.input_img_signed_url;
      outputImageUrl.value = latest.output_img_signed_url;
      completedGenerationId.value = latest.id;
    } 
    else if (latest.status === 'failed') {
      inputImageUrl.value = latest.input_img_signed_url;
      toast.info(latest.error_api_message || latest.error_message);
      clearStopEnableTimer();
    }
    else if (latest.status === 'stopped_by_user') {
      inputImageUrl.value = latest.input_img_signed_url;
      clearStopEnableTimer();
    }
    else if (latest.status === 'rejected_by_safety') {
      inputImageUrl.value = latest.input_img_signed_url;
      toast.info(latest.error_api_message);
      clearStopEnableTimer();
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

const stopPolling = () => {
  if (pollingTimeoutId) {
    clearTimeout(pollingTimeoutId);
    pollingTimeoutId = null;
  }
};

const pollForResult = async () => {
  if (pollAttempt >= POLL_INTERVALS_MS.length) {
    stopPolling();
    isLoading.value = false;
    currentGenerationId.value = null;
    toast.info('Failed to get the generated image. Please try again later.'); //чи треба це взагалі?
    clearStopEnableTimer();
    return;
  }

  try {
    const response = await api.get('/api/generations/generation-requests/latest/');
    const latest = response.data;
    
    if (latest?.status === 'failed') {
      toast.info(latest.error_api_message || latest.error_message);
      isLoading.value = false;
      stopPolling();
      currentGenerationId.value = null;
      clearStopEnableTimer();
    }
    else if (latest?.status === 'stopped_by_user') {
        isLoading.value = false;
        stopPolling();
        currentGenerationId.value = null;
        clearStopEnableTimer();
    }
    else if (latest?.status === 'rejected_by_safety') {
        toast.info(latest.error_api_message);
        isLoading.value = false;
        stopPolling();
        currentGenerationId.value = null;
        clearStopEnableTimer();
    }
    else if (latest?.status === 'completed' && latest.output_img_signed_url) {
      outputImageUrl.value = latest.output_img_signed_url;
      completedGenerationId.value = latest.id;
      if (latest.input_img_signed_url && !inputImageUrl.value) {
          inputImageUrl.value = latest.input_img_signed_url;
      }
      isLoading.value = false;
      stopPolling();
      currentGenerationId.value = null;
      clearStopEnableTimer();
    } 
    else {
      const nextInterval = POLL_INTERVALS_MS[pollAttempt];
      pollAttempt++;
      pollingTimeoutId = setTimeout(pollForResult, nextInterval);
    }
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'An unexpected error occurred while checking generation status.';
    toast.info(errorMessage);
    isLoading.value = false;
    stopPolling();
    currentGenerationId.value = null;
    clearStopEnableTimer();
  }
};

const startPolling = () => {
  stopPolling();
  pollAttempt = 0;
  pollForResult();
};

onUnmounted(() => {
  stopPolling();
  clearStopEnableTimer();
});

const buttonText = computed(() => {
  if (!isLoading.value) {
    return 'Transform';
  }
  if (isStoppingAllowed.value) {
    return 'Stop transformation';
  }
  return 'Transforming...';
});

const isButtonDisabled = computed(() => {
  return isLoading.value && !isStoppingAllowed.value;
});

const startStopEnableTimer = (creationTime) => {
  clearStopEnableTimer();
  isStoppingAllowed.value = false;

  if (creationTime) {
    const createdAt = new Date(creationTime);
    const now = new Date();
    const elapsedTime = now.getTime() - createdAt.getTime();
    const remainingTime = 30000 - elapsedTime;

    if (remainingTime <= 0) {
      isStoppingAllowed.value = true;
    } else {
      stopEnableTimerId = setTimeout(() => {
        isStoppingAllowed.value = true;
      }, remainingTime);
    }
  } else {
    stopEnableTimerId = setTimeout(() => {
      isStoppingAllowed.value = true;
    }, 30000);
  }
};

const clearStopEnableTimer = () => {
  clearTimeout(stopEnableTimerId);
  stopEnableTimerId = null;
};

const handleButtonClick = () => {
  if (!isLoading.value) {
    handleGenerate();
  } 
  else {
    handleStopGeneration();
  }
};

const getErrorMessage = (err, endpoint) => {
  if (!err.response) {
    return null;
  }

  const { status, data } = err.response;
  const serverError = data?.detail;

  if (status === 400) {
    if (endpoint === 'create') {
      return serverError || data?.non_field_errors?.[0] || 'Could not create request. Please try again later.';
    } 
    else if (endpoint === 'stop') {
      return serverError || 'Could not stop generation. Please try again later.';
    } 
    else if (endpoint === 'download') {
      return serverError || 'Could not download the image. Please try again later.';
    }
  } 
  else if (status === 404) {
    if (endpoint === 'stop') {
      return serverError || 'Generation request not found. Please try again later.';
    } 
    else if (endpoint === 'download') {
      return serverError || 'File for download not found. Please try again later.';
    }
  }
  return null;
};

const handleStopGeneration = async () => {
  clearStopEnableTimer();
  if (!currentGenerationId.value) {
    stopPolling();
    isLoading.value = false;
    return;
  }
  try {
    await api.post(`/api/generations/generation-requests/stop/${currentGenerationId.value}/`);
    stopPolling();
    isLoading.value = false;
    currentGenerationId.value = null;
  } catch (err) {
    stopPolling();
    isLoading.value = false;
    currentGenerationId.value = null;
    
    if (err.response && [400, 404].includes(err.response.status)) {
      toast.info(getErrorMessage(err, 'stop'));
    }
  }
};

const handleGenerate = async () => {
  if (isLoading.value) return;
  if ((!inputImageFile.value && !inputImageUrl.value) || !props.selectedStyleId) {
    toast.info('Choose your picture and destiny');
    return;
  }
  isLoading.value = true;
  outputImageUrl.value = null;
  completedGenerationId.value = null;
  startStopEnableTimer();

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

  } catch (err) {
    isLoading.value = false;
    if (err.response && err.response.status === 400) {
        toast.info(getErrorMessage(err, 'create'));
    }
  }
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const onFileSelected = (event) => {
  const target = event.target;
  const file = target.files?.[0];
  handleFile(file);
};

const handleFile = (file) => {
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
};

const onDragEnter = (event) => {
  event.preventDefault();
  isDragging.value = true;
};

const onDragOver = (event) => {
  event.preventDefault(); 
};

const onDragLeave = (event) => {
  event.preventDefault();
  isDragging.value = false;
};

const onDrop = (event) => {
  event.preventDefault();
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  handleFile(file);
};

const onInputImageLoad = () => {
  inputImageLoaded.value = true;
};

const onOutputImageLoad = () => {
  outputImageLoaded.value = true;
};

const downloadOutputImage = async () => {
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
  } catch (err) {
    if (err.response && [400, 404].includes(err.response.status)) {
      toast.info(getErrorMessage(err, 'download'));
    }
  }
};
</script>

<style scoped>
@keyframes wave {
  0%, 100% { transform: rotate(35deg)}
  25% { transform: rotate(50deg)}
  75% { transform: rotate(40deg)}
  50% {
    opacity: 0.45;
  }
}

.wave-animation {
  animation: wave 1.6s ease-in-out infinite;
}

.border-gradient-animated {
  border: 2px solid #3A1078;
  animation: borderGradient 3s ease-in-out infinite;
}

@keyframes borderGradient {
  0%, 100% { 
    border-color: #3A1078;
  }
  25% { 
    border-color: #4E31AA;
  }
  50% { 
    border-color: #3795BD;
  }
  75% { 
    border-color: #4E31AA;
  }
}

@media (max-width: 380px) { 
  .modal-text {
    font-size: 1rem;
    line-height: 1.4;
    word-break: break-word;
  }
}

</style>
