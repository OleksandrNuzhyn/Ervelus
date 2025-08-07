<template>
  <div class="mt-4 md:mt-8 p-2 md:p-4">
    <div class="flex flex-col lg:grid lg:grid-cols-2 gap-8 items-start">
      <!-- Input Image Section -->
      <div class="flex flex-col items-center w-full">
        <div class="bg-transparent backdrop-blur-[14px] bg-[rgba(31,41,55,0.3)] rounded-lg p-4 h-[400px] md:h-[660px] w-full flex flex-col items-center justify-center">
          <div v-if="!inputImageUrl" @click="triggerFileInput" class="cursor-pointer w-full h-full flex flex-col items-center justify-center">
            <svg class="w-16 h-16 md:w-24 md:h-24 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
            </svg>
            <p class="mt-4 text-lg text-gray-400">Click here</p>
            <input type="file" ref="fileInput" @change="onFileSelected" class="hidden" accept="image/*" />
          </div>
          <div v-else class="relative w-full h-full">
            <img :src="inputImageUrl" alt="Input" class="w-full h-full object-contain rounded-lg" />
             <button @click="inputImageUrl = null" class="absolute top-2 right-2 bg-red-600 hover:bg-red-700 text-white font-bold p-2 rounded-full text-xs">
              X
            </button>
          </div>
        </div>
        <div
          v-if="selectedStyleName"
          class="w-full bg-gray-700 text-white rounded-xl py-3 md:py-4 mt-5 text-center text-base md:text-lg font-medium"
        >
          {{ selectedStyleName }}
        </div>
      </div>

      <!-- Output Image Section -->
      <div class="flex flex-col w-full">
        <div class="flex flex-col items-center justify-center bg-gray backdrop-blur-[14px] bg-[rgba(31,41,55,0.3)] rounded-lg p-4 h-[400px] md:h-[660px]">
          <div v-if="isLoading" class="flex flex-col items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-10 w-10 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="mt-2 text-lg">Генерація...</p>
          </div>
          <div v-else-if="outputImageUrl" class="w-full h-full">
            <img :src="outputImageUrl" alt="Output" class="w-full h-full object-contain rounded-lg" />
          </div>
          <div v-else class="text-center text-gray-400">
            <p>Результат генерації з'явиться тут</p>
          </div>
        </div>
        <div class="mt-5 flex flex-col sm:flex-row justify-between items-center gap-5">
          <div class="flex justify-center w-full sm:w-auto space-x-3 text-white">
            <button @click="selectedAspectRatio = '1:1'" :class="[ 'px-4 py-2 sm:px-8 sm:py-3 md:px-12 md:py-4 rounded-lg border transition-colors flex-grow sm:flex-grow-0', selectedAspectRatio === '1:1' ? 'bg-blue-600 border-blue-600' : 'bg-gray-700 border-gray-600 hover:bg-gray-600' ]">
              1:1
            </button>
            <button @click="selectedAspectRatio = '2:3'" :class="[ 'px-4 py-2 sm:px-8 sm:py-3 md:px-12 md:py-4 rounded-lg border transition-colors flex-grow sm:flex-grow-0', selectedAspectRatio === '2:3' ? 'bg-blue-600 border-blue-600' : 'bg-gray-700 border-gray-600 hover:bg-gray-600' ]">
              2:3
            </button>
            <button @click="selectedAspectRatio = '3:2'" :class="[ 'px-4 py-2 sm:px-8 sm:py-3 md:px-12 md:py-4 rounded-lg border transition-colors flex-grow sm:flex-grow-0', selectedAspectRatio === '3:2' ? 'bg-blue-600 border-blue-600' : 'bg-gray-700 border-gray-600 hover:bg-gray-600' ]">
              3:2
            </button>
          </div>
          <button
            @click="handleGenerate"
            :disabled="!inputImageUrl || isLoading"
            class="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white font-bold py-3 md:py-4 px-8 rounded-lg transition-colors text-lg md:text-xl disabled:bg-gray-500 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Генерація...' : 'Згенерувати' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue';

defineProps({
  selectedStyleName: {
    type: String,
    required: false,
    default: null,
  },
});

const inputImageUrl = ref(null);
const outputImageUrl = ref(null);
const isLoading = ref(false);
const fileInput = ref(null);
const selectedAspectRatio = ref('1:1');

const handleGenerate = () => {
  isLoading.value = true;
  outputImageUrl.value = null;

  const getDimensions = (ratio) => {
    const baseSize = 512;
    const [w, h] = ratio.split(':').map(Number);
    let width, height;

    if (w > h) {
      width = baseSize;
      height = Math.round((baseSize * h) / w);
    } else if (h > w) {
      width = Math.round((baseSize * w) / h);
      height = baseSize;
    } else {
      width = height = baseSize;
    }
    return { width, height };
  };

  const { width, height } = getDimensions(selectedAspectRatio.value);

  setTimeout(() => {
    outputImageUrl.value = `https://picsum.photos/seed/${Math.random()}/${width}/${height}`;
    isLoading.value = false;
  }, 2000);
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const onFileSelected = (event) => {
  const target = event.target;
  const file = target.files?.[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      inputImageUrl.value = e.target?.result;
    };
    reader.readAsDataURL(file);
  }
};
</script>
