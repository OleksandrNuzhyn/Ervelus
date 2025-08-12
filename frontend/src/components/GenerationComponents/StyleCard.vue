<script setup>
const props = defineProps({
  styleData: {
    type: Object,
    required: true,
  },
  isSelected: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['select-style']);

const selectStyle = () => {
  emit('select-style', props.styleData.id);
};
</script>

<template>
  <div
    @click="selectStyle"
    class="relative cursor-pointer transition-all duration-200 ease-in-out transform hover:scale-105"
  >
    <!-- Заокруглений квадрат -->
    <div 
      class="w-32 h-32 rounded-2xl bg-gray-700 mx-auto transition-all duration-200 flex items-center justify-center"
      :class="[
        isSelected ? 'ring-4 ring-blue-500 ring-opacity-80' : 'hover:ring-2 hover:ring-gray-500 hover:ring-opacity-50',
      ]"
    >
      <!-- Плейсхолдер з першою літерою назви -->
      <span class="text-gray-300 text-2xl font-bold">
        {{ styleData.name?.charAt(0) || '?' }}
      </span>
    </div>
    
    <!-- Назва стилю -->
    <div class="mt-3 text-center">
      <span class="text-white text-sm font-semibold">{{ styleData.name }}</span>
    </div>
    
    <!-- PRO мітка -->
    <div
      v-if="styleData.isPro"
      class="absolute top-0 right-2 bg-yellow-500 text-gray-900 text-xs font-bold px-2 py-1 rounded-full"
    >
      PRO
    </div>
  </div>
</template> 