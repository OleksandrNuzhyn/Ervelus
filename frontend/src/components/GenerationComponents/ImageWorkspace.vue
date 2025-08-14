<template>
  <div class="mt-4 md:mt-8 p-2 md:p-4">
    <div v-if="error" class="bg-red-500 text-white p-3 rounded-lg mb-4 text-center">
      {{ error }}
    </div>
    <div class="flex flex-col lg:grid lg:grid-cols-2 gap-8 items-start">
      <div class="flex flex-col items-center w-full">
        <div class="bg-transparent backdrop-blur-[14px] bg-[rgba(31,41,55,0.3)] rounded-lg p-4 h-[400px] md:h-[660px] w-full flex flex-col items-center justify-center">
          <div v-if="!inputImageUrl" @click="triggerFileInput" class="cursor-pointer w-full h-full flex flex-col items-center justify-center">
            <svg class="w-16 h-16 md:w-24 md:h-24 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
            </svg>
            <p class="mt-4 text-lg text-gray-400">Click here to upload</p>
            <input type="file" ref="fileInput" @change="onFileSelected" class="hidden" accept="image/jpeg, image/png, image/webp" />
          </div>
          <div v-else class="relative w-full h-full">
            <img :src="inputImageUrl" alt="Input" class="w-full h-full object-contain rounded-lg" />
            <button @click="inputImageUrl = null" class="absolute top-2 right-2 bg-transparent text-gray-400 hover:text-white p-2 transition-colors">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            </button>
          </div>
        </div>
        <div
          v-if="selectedStyleName"
          class="w-full bg-gray-800 text-white rounded-xl py-3 md:py-4 mt-5 text-center text-base md:text-lg font-medium"
        >
          {{ selectedStyleName }}
        </div>
      </div>

      <div class="flex flex-col w-full">
        <div class="flex flex-col items-center justify-center bg-transparent backdrop-blur-[14px] bg-[rgba(31,41,55,0.3)] rounded-lg p-4 h-[400px] md:h-[660px]">
          <div v-if="isLoading" class="flex flex-col items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-10 w-10 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938л3-2.647з"></path>
            </svg>
            <p class="mt-2 text-lg">Generating...</p>
          </div>
          <div v-else-if="outputImageUrl" class="w-full h-full">
            <img :src="outputImageUrl" alt="Output" class="w-full h-full object-contain rounded-lg" />
          </div>
          <div v-else class="text-center text-gray-400">
            <p>The result of the generation will appear here</p>
          </div>
        </div>
        <div class="mt-5 flex flex-col sm:flex-row justify-between items-center gap-5">
          <div class="flex justify-center w-full sm:w-auto space-x-3 text-white">
            <button @click="selectedAspectRatio = '1:1'" :class="[ 'px-4 py-2 sm:px-8 sm:py-3 md:px-12 md:py-4 rounded-lg border transition-colors flex-grow sm:flex-grow-0', selectedAspectRatio === '1:1' ? 'bg-gray-600 border-gray-400' : 'bg-gray-800 border-gray-600 hover:bg-gray-600' ]">
              1:1
            </button>
            <button @click="selectedAspectRatio = '2:3'" :class="[ 'px-4 py-2 sm:px-8 sm:py-3 md:px-12 md:py-4 rounded-lg border transition-colors flex-grow sm:flex-grow-0', selectedAspectRatio === '2:3' ? 'bg-gray-600 border-gray-400' : 'bg-gray-800 border-gray-600 hover:bg-gray-600' ]">
              2:3
            </button>
            <button @click="selectedAspectRatio = '3:2'" :class="[ 'px-4 py-2 sm:px-8 sm:py-3 md:px-12 md:py-4 rounded-lg border transition-colors flex-grow sm:flex-grow-0', selectedAspectRatio === '3:2' ? 'bg-gray-600 border-gray-400' : 'bg-gray-800 border-gray-600 hover:bg-gray-600' ]">
              3:2
            </button>
          </div>
          <button
            @click="handleGenerate"
            :disabled="isLoading"
            class="w-full sm:w-auto bg-gradient-to-r from-purple-800 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white font-bold py-3 md:py-4 px-8 rounded-lg transition-colors text-lg md:text-xl disabled:bg-gray-500 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Generating...' : 'Generate' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="showMissingInfoModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0" @click="showMissingInfoModal = false"></div>
      <div class="relative bg-gray-800/90 text-white rounded-2xl px-6 py-5 text-center max-w-sm w-full">
        <p class="text-lg md:text-xl font-medium">Choose your picture and destiny<br> from the list on top</p>
        <button @click="showMissingInfoModal = false" class="mt-4 px-4 py-2 bg-gray-600 rounded-lg hover:bg-gray-700 transition-colors">Got it!</button>
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
      return;
    }
    
    try {
      const response = await api.get('/api/generations/generation-requests/latest/');
      const latest = response.data;
      
      if (latest?.status === 'failed') {
        error.value = latest.error || 'Generation failed on the backend.';
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
        // єбашим гойз
      }
    } catch (err) {
        error.value = 'Failed to get the generated image. Please try again.';
        isLoading.value = false;
        stopPolling();
    }
  }, POLL_INTERVAL_MS);
};

onMounted(async () => {
    try {
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
            }
        }
    } catch(err) {
        console.log("Could not fetch latest generation, maybe there are none.", err);
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

  try {
    const resolution = resolutionMap[selectedAspectRatio.value];
    const formData = new FormData();
    formData.append('chosen_style', props.selectedStyleId);
    formData.append('input_image', inputImageFile.value);
    formData.append('resolution', resolution);

    await api.post('/api/generations/generation-requests/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    
    setTimeout(startPolling, 30000);

  } catch (err) {
    isLoading.value = false;
    error.value = err.response?.data?.error || 'Generation failed. Please try again.';
  }
};

const triggerFileInput = () => {
  error.value = null;
  fileInput.value?.click();
};

const onFileSelected = (event) => {
  const target = event.target;
  const file = target.files?.[0];
  if (!file) {
    return;
  }

  error.value = null;

  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    error.value = 'Invalid file type. Please select an image in JPEG, PNG or WEBP format.';
    return;
  }
  else if (file.size > MAX_FILE_SIZE_BYTES) {
    error.value = 'File size is too large. Maximum size is 10 MB.';
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
