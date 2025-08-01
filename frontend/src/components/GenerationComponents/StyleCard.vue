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
    class="relative cursor-pointer rounded-lg overflow-hidden transition-all duration-200 ease-in-out transform hover:scale-105"
    :class="[
      isSelected ? 'border-4 border-blue-500 shadow-lg' : 'border-2 border-gray-700 hover:border-gray-500',
    ]"
  >
    <img :src="styleData.previewUrl" :alt="styleData.name" class="w-full h-auto object-cover" />
    <div class="absolute bottom-0 left-0 right-0 p-2 bg-black bg-opacity-50">
      <span class="text-white text-sm font-semibold">{{ styleData.name }}</span>
    </div>
    <div
      v-if="styleData.isPro"
      class="absolute top-2 right-2 bg-yellow-500 text-gray-900 text-xs font-bold px-2 py-1 rounded"
    >
      PRO
    </div>
  </div>
</template> 