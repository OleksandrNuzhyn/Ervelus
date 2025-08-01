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

<template>
  <div class="mt-8 p-4">
    <div class="grid grid-cols-2 gap-8 items-start">
      <!-- Input Column -->
      <div class="flex flex-col items-center w-full">
        <!-- прямокутник поля зображення -->
        <div class="bg-transparent backdrop-blur-[14px] bg-[rgba(10,10,10,0.3)] rounded-lg p-4 h-[600px] w-full flex flex-col items-center justify-center">
          <div v-if="!inputImageUrl" class="text-center">
            <button @click="triggerFileInput" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors">
              Завантажити зображення
            </button>
            <input type="file" ref="fileInput" @change="onFileSelected" class="hidden" accept="image/*" />
          </div>
          <div v-else class="relative w-full h-full">
            <img :src="inputImageUrl" alt="Input" class="w-full h-full object-contain rounded-lg" />
             <button @click="inputImageUrl = null" class="absolute top-2 right-2 bg-red-600 hover:bg-red-700 text-white font-bold p-2 rounded-full text-xs">
              X
            </button>
          </div>
        </div>
        <!-- Прямокутник з назвою стилю одразу під полем -->
        <div
          v-if="selectedStyleName"
          class="w-full bg-gray-700 text-white rounded-xl py-4 mt-3 text-center text-lg font-medium"
        >
          {{ selectedStyleName }}
        </div>
      </div>

      <!-- Output Column -->
      <div class="flex flex-col">
        <div class="flex flex-col items-center justify-center bg-transparent backdrop-blur-[14px] bg-[rgba(10,10,10,0.3)] rounded-lg p-4 h-[600px]">
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
        <div class="mt-3 flex justify-between items-center ">
          <div class="flex space-x-10 text-white ">
            <button @click="selectedAspectRatio = '1:1'" :class="[ 'px-12 py-4 rounded-lg border transition-colors', selectedAspectRatio === '1:1' ? 'bg-blue-600 border-blue-600' : 'bg-gray-700 border-gray-600 hover:bg-gray-600' ]">
              1:1
            </button>
            <button @click="selectedAspectRatio = '2:3'" :class="[ 'px-12 py-4 rounded-lg border transition-colors', selectedAspectRatio === '2:3' ? 'bg-blue-600 border-blue-600' : 'bg-gray-700 border-gray-600 hover:bg-gray-600' ]">
              2:3
            </button>
            <button @click="selectedAspectRatio = '3:2'" :class="[ 'px-12 py-4 rounded-lg border transition-colors', selectedAspectRatio === '3:2' ? 'bg-blue-600 border-blue-600' : 'bg-gray-700 border-gray-600 hover:bg-gray-600' ]">
              3:2
            </button>
          </div>
          <button
            @click="handleGenerate"
            :disabled="!inputImageUrl || isLoading"
            class="bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-8 rounded-lg transition-colors text-xl disabled:bg-gray-500 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Генерація...' : 'Згенерувати' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template> 