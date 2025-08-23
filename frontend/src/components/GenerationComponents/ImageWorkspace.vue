<template>
  <div class="mt-2 p-3">
    <div class="flex flex-col lg:grid lg:grid-cols-2 gap-8 items-start">
      <div class="flex flex-col items-center w-full">
        <div class="bg-black/30 backdrop-blur-[7px] shadow-[0_0_5px_rgba(0,0,0)] rounded-lg p-4 h-[400px] md:h-[660px] w-full flex flex-col items-center justify-center">
          <div v-if="!inputImageUrl" @click="triggerFileInput" class="cursor-pointer w-full h-full flex flex-col items-center justify-center">
            <svg class="w-16 h-16 md:w-24 md:h-24 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
            </svg>
            <p class="mt-4 text-lg text-gray-400">Click here to upload</p>
            <input type="file" ref="fileInput" @change="onFileSelected" class="hidden" accept="image/jpeg, image/png, image/webp" />
          </div>
          <div v-else class="relative w-full h-full">
            <img :src="inputImageUrl" alt="Input" class="w-full h-full object-contain rounded-lg" />
            <button @click="inputImageUrl = null; outputImageUrl = null" class="absolute top-1 right-1 bg-gray-800/80 hover:bg-gray-700/90 text-gray-300 hover:text-white p-1.5 transition-colors rounded border border-gray-600/50 hover:border-gray-500">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            </button>
          </div>
        </div>
        <div
          v-if="selectedStyleName"
            class="w-full bg-black/30 backdrop-blur-[7px] shadow-[0_0_5px_rgba(0,0,0)] rounded-xl py-3 lg:py-6 mt-5 text-center text-xl md:text-2xl font-bold"
          >
          {{ selectedStyleName }}
        </div>
      </div>

      <div class="flex flex-col w-full">
        <div class="flex flex-col items-center justify-center bg-black/30 backdrop-blur-[7px] shadow-[0_0_5px_rgba(0,0,0)] rounded-lg p-4 h-[400px] md:h-[660px]">
          <div v-if="isLoading" class="flex flex-col items-center justify-center">
            <img src="@/assets/svg/staff_logo.svg" class="wave-animation animation-pulse h-45 w-45 pointer-events-none select-none" />
            <p class="text-gray-400 text-lg">Generating...</p>
          </div>
          <div v-else-if="outputImageUrl" class="w-full h-full">
            <img :src="outputImageUrl" alt="Output" class="w-full h-full object-contain rounded-lg" />
          </div>
          <div v-else class="text-center text-gray-400">
            <p>The result of the generation will appear here</p>
          </div>
        </div>
        <div class="mt-7 mb-2 flex flex-col sm:flex-row justify-center sm:justify-between items-center gap-8 sm:gap-5 md:gap-6 lg:gap-10">
          <div class="flex justify-center w-full md:pl-5 xl:pl-10 2xl:pl-15 sm:w-auto gap-15 text-white flex-shrink-0">
            <button @click="selectedAspectRatio = '1:1'" :aria-label="'Aspect ' + '1:1'" :class="[ 'relative w-12 h-12 sm:w-12 sm:h-12 md:w-14 md:h-14 transition-all duration-200 group', selectedAspectRatio === '1:1' ? 'scale-103' : 'hover:scale-100' ]">
              <span class="absolute -inset-1 rounded-md border-2 pointer-events-none transform rotate-45 transition-opacity duration-200 group-hover:opacity-100 border-[#03346E] opacity-0" :class="[ selectedAspectRatio === '1:1' ? 'opacity-100' : '' ]"></span>
              <span class="absolute inset-0 rounded-md bg-gradient-to-br from-[#021526] via-[#03346E] to-[#6EACDA]/80 shadow-md shadow-[#021526]/50 transform rotate-45"></span>
              <span class="absolute inset-[3px] rounded-[6px] bg-[#6EACDA]/10 transform rotate-45"></span>
              <span class="relative z-10 transform rotate-0 text-xs sm:text-sm md:text-base font-semibold pointer-events-none select-none">1:1</span>
            </button>
            <button @click="selectedAspectRatio = '2:3'" :aria-label="'Aspect ' + '2:3'" :class="[ 'relative w-12 h-12 sm:w-12 sm:h-12 md:w-14 md:h-14 transition-all duration-200 group', selectedAspectRatio === '2:3' ? 'scale-103' : 'hover:scale-100' ]">
              <span class="absolute -inset-1 rounded-md border-2 pointer-events-none transform rotate-45 transition-opacity duration-200 group-hover:opacity-100 border-[#2E236C] opacity-0" :class="[ selectedAspectRatio === '2:3' ? 'opacity-100' : '' ]"></span>
              <span class="absolute inset-0 rounded-md bg-gradient-to-br from-[#17153B] via-[#2E236C] to-[#D4ADFC]/80 shadow-md shadow-[#17153B]/50 transform rotate-45"></span>
              <span class="absolute inset-[3px] rounded-[6px] bg-[#C8ACD6]/10 transform rotate-45"></span>
              <span class="relative z-10 transform rotate-0 text-xs sm:text-sm md:text-base font-semibold pointer-events-none select-none">2:3</span>
            </button>
            <button @click="selectedAspectRatio = '3:2'" :aria-label="'Aspect ' + '3:2'" :class="[ 'relative w-12 h-12 sm:w-12 sm:h-12 md:w-14 md:h-14 transition-all duration-200 group', selectedAspectRatio === '3:2' ? 'scale-103' : 'hover:scale-100' ]">
              <span class="absolute -inset-1 rounded-md border-2 pointer-events-none transform rotate-45 transition-opacity duration-200 group-hover:opacity-100 border-[#055052] opacity-0" :class="[ selectedAspectRatio === '3:2' ? 'opacity-100' : '' ]"></span>
              <span class="absolute inset-0 rounded-md bg-gradient-to-br from-[#003638] via-[#055052] to-[#53B8BB]/90 shadow-md shadow-[#003638]/50 transform rotate-45"></span>
              <span class="absolute inset-[3px] rounded-[6px] bg-[#9DB2BF]/10 transform rotate-45"></span>
              <span class="relative z-10 transform rotate-0 text-xs sm:text-sm md:text-base font-semibold pointer-events-none select-none">3:2</span>
            </button>
          </div>
          <button 
            @click="handleGenerate"
            :disabled="isLoading"
            :class="[
              'relative px-4 py-4 sm:px-6 md:px-8 transition-all min-w-[100px] w-[140px] md:h-[65px] sm:w-[160px] md:w-[160px] lg:w-[180px] xl:w-[200px] duration-200 rounded-xl generate-button flex items-center justify-center',
              isLoading ? 'scale-100' : 'group hover:scale-100'
            ]"
          >
            <span 
              v-if="!isLoading"
              :class="[
                'absolute -inset-1 rounded-xl border-3 pointer-events-none transition-all duration-100',
                'group-hover:opacity-100 opacity-90',
                selectedAspectRatio === '1:1' ? 'border-[#03346E]' : 
                selectedAspectRatio === '2:3' ? 'border-[#2E236C]' : 
                'border-[#055052]'
              ]"
            ></span>
            <span 
              v-if="isLoading"
              class="absolute -inset-0.5 rounded-xl pointer-events-none opacity-70 border-gradient-animated"
              :style="{
                '--start-color': selectedAspectRatio === '1:1' ? '#03346E' : 
                                selectedAspectRatio === '2:3' ? '#2E236C' : '#055052'
              }"
            ></span>
            <span 
              class="absolute inset-0 rounded-xl bg-transparent backdrop-blur-[1px] shadow-lg"
            ></span>
            <span 
              class="absolute inset-[1px] rounded-[5px] bg-gray-400/30"
            ></span>
            <span 
              class="relative z-10 text-sm md:text-base text-center font-semibold pointer-events-none select-none text-white"
            >
              {{ isLoading ? 'Generating...' : 'Generate' }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showMissingInfoModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0" @click="showMissingInfoModal = false"></div>
      <div class="relative bg-gray-800/90 backdrop-blur-[14px] border border-gray-700 shadow-xl shadow-gray-600/50 text-white rounded-2xl px-6 py-5 text-center max-w-sm w-full">
        <svg class="absolute top-5 left-3 w-7 h-7 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="9" stroke-width="2"></circle>
          <path d="M12 7v6" stroke-linecap="round" stroke-width="2"></path>
          <circle cx="12" cy="17" r="1.25" fill="currentColor" stroke="none"></circle>
        </svg>
        <p class="modal-text text-lg md:text-xl font-medium">Choose your picture and destiny<br> from the list on top</p>
        <button @click="showMissingInfoModal = false" class="modal-button mt-4 px-4 py-2 font-bold text-white transition duration-300 rounded-md disabled:opacity-60 disabled:cursor-not-allowed bg-white/10 backdrop-blur-md border border-white/1 shadow-lg hover:bg-white/20">Got it!</button>
      </div>
    </div>

    <div v-if="showErrorModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0" @click="showErrorModal = false"></div>
      <div class="relative bg-gray-800/90 backdrop-blur-[14px] border border-gray-700 shadow-xl shadow-gray-600/50 text-white rounded-2xl px-6 py-5 text-center max-w-sm w-full">
        <svg class="absolute top-1 left-1/2 -translate-x-1/2 w-7 h-7 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="9" stroke-width="2"></circle>
          <line x1="15" y1="9" x2="9" y2="15" stroke-width="2"></line>
          <line x1="9" y1="9" x2="15" y2="15" stroke-width="2"></line>
        </svg>
        <p class="modal-text text-lg mt-3 font-medium">{{ error }}</p>
        <button @click="showErrorModal = false; error = null" class="modal-button mt-4 px-4 py-2 font-bold text-white transition duration-300 rounded-md disabled:opacity-60 disabled:cursor-not-allowed bg-white/10 backdrop-blur-md border border-white/1 shadow-lg hover:bg-white/20">OK</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import api from '@/services/api';

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
  }
});

const inputImageUrl = ref(null);
const inputImageFile = ref(null);
const outputImageUrl = ref(null);
const isLoading = ref(false);
const fileInput = ref(null);
const selectedAspectRatio = ref('1:1');
const error = ref(null);
const showMissingInfoModal = ref(false);
const showErrorModal = ref(false);

const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024;
const POLL_INTERVAL_MS = 3000;
const MAX_POLL_ATTEMPTS = 40;
let pollingIntervalId = null;

watch(inputImageUrl, (newVal) => {
  if (!newVal) {
    inputImageFile.value = null;
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
});

const stopPolling = () => {
  if (pollingIntervalId) {
    clearInterval(pollingIntervalId);
    pollingIntervalId = null;
  }
};

const startPolling = () => {
  stopPolling(); 

  let attempts = 0;
  pollingIntervalId = setInterval(async () => {
    attempts++;

    if (attempts > MAX_POLL_ATTEMPTS) {
      stopPolling();
      isLoading.value = false;
      error.value = 'Failed to get the generated image. Please try again.';
      showErrorModal.value = true;
      return;
    }
    
    try {
      const response = await api.get('/api/generations/generation-requests/latest/');
      const latest = response.data;
      
      if (latest?.status === 'failed') {
        error.value = latest.error || 'Generation failed on the backend.';
        showErrorModal.value = true;
        isLoading.value = false;
        stopPolling();
      } 
      else if (latest?.status === 'completed' && latest.output_img_signed_url) {
        outputImageUrl.value = latest.output_img_signed_url;
        if (latest.input_img_signed_url && !inputImageUrl.value) {
            inputImageUrl.value = latest.input_img_signed_url;
        }
        isLoading.value = false;
        stopPolling();
      } 
      else if (latest?.status === 'processing') {
        // continue polling
      }
    } catch (err) {
        error.value = 'Failed to get the generated image. Please try again.';
        showErrorModal.value = true;
        isLoading.value = false;
        stopPolling();
    }
  }, POLL_INTERVAL_MS);
};

onMounted(async () => {
  const response = await api.get('/api/generations/generation-requests/latest/');
  const latest = response.data;
  
  if (latest) {
    if (latest.status === 'processing') {
        isLoading.value = true;
        inputImageUrl.value = latest.input_img_signed_url;
        outputImageUrl.value = null;
        error.value = null;
        startPolling();
    } else if (latest.status === 'completed' && latest.output_img_signed_url) {
        inputImageUrl.value = latest.input_img_signed_url;
        outputImageUrl.value = latest.output_img_signed_url;
    } else if (latest.status === 'failed') {
        inputImageUrl.value = latest.input_img_signed_url;
        error.value = latest.error || 'The last generation has failed.';
        showErrorModal.value = true;
    }
  }
});

onUnmounted(() => {
  stopPolling();
});

const resolutionMap = {
  '1:1': '1024x1024',
  '2:3': '1024x1536',
  '3:2': '1536x1024',
};

const handleGenerate = async () => {
  if (!inputImageFile.value || !props.selectedStyleId) {
    showMissingInfoModal.value = true;
    return;
  }
  isLoading.value = true;
  outputImageUrl.value = null;
  error.value = null;
  showErrorModal.value = false;

  try {
    const resolution = resolutionMap[selectedAspectRatio.value];
    const formData = new FormData();
    formData.append('chosen_style', props.selectedStyleId);
    formData.append('input_image', inputImageFile.value);
    formData.append('resolution', resolution);

    await api.post('/api/generations/generation-requests/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    
    setTimeout(startPolling, 20000);

  } catch (err) {
    isLoading.value = false;
    error.value = err.response?.data?.error || 'Generation failed. Please try again.';
    showErrorModal.value = true;
  }
};

const triggerFileInput = () => {
  error.value = null;
  showErrorModal.value = false;
  fileInput.value?.click();
};

const onFileSelected = (event) => {
  const target = event.target;
  const file = target.files?.[0];
  if (!file) {
    return;
  }

  error.value = null;
  showErrorModal.value = false;

  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    error.value = 'Invalid file type. Please select an image in JPEG, PNG or WEBP format.';
    showErrorModal.value = true;
    return;
  }
  else if (file.size > MAX_FILE_SIZE_BYTES) {
    error.value = 'File size is too large. Maximum size is 10 MB.';
    showErrorModal.value = true;
    return;
  }

  inputImageFile.value = file;
  const reader = new FileReader();
  reader.onload = (event) => {
    inputImageUrl.value = event.target?.result;
  };
  reader.readAsDataURL(file);
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

@media (min-width: 1800px) {
  .generate-button {
    margin-right: 120px;
  }
}
</style>
