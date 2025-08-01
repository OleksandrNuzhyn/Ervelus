<script setup>
import StyleCard from './StyleCard.vue';

defineProps({
  styles: {
    type: Array,
    required: true,
  },
  selectedStyleId: {
    type: String,
    required: false,
    default: null
  },
});

const emit = defineEmits(['style-selected','close']);

const onStyleSelected = (styleId) => {
  emit('style-selected', styleId);
};
const handleClose = ()=>{
  emit('close');
}
</script>

<template>
  <div class="bg-transparent backdrop-blur-[14px] bg-[rgba(10,10,10,0.3)] rounded-xl shadow-lg p-4 h-[calc(100vh-10rem)] overflow-y-auto">
      <div class="flex justify-between items-center mb-6 px-2">
        <h2 class="text-2xl font-bold text-white">Виберіть стиль</h2>
        <button @click="handleClose" class="text-white bg-gray-700 hover:bg-gray-600 rounded-full p-2 transition-colors">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <StyleCard
          v-for="style in styles"
          :key="style.id"
          :style-data="style"
          :is-selected="style.id === selectedStyleId"
          @select-style="onStyleSelected"
        />
    </div>
  </div>
</template> 