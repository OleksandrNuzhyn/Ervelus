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

const getSpriteClass = () => {
  if (props.styleData.name) {
    const className = props.styleData.name
      .toLowerCase()
      .replace(/\s+/g, '_')
      .replace(/[^a-z0-9_]/g, '');
    const cssClass = `bg-${className}`;
        
    return cssClass;
  }
  return '';
};
</script>

<template>
  <div
    @click="selectStyle"
    class="relative cursor-pointer transition-all duration-200 ease-in-out transform hover:scale-105"
  >
    <!-- Заокруглений квадрат -->
    <div 
      class="w-32 h-32 rounded-2xl mx-auto transition-all duration-200 flex items-center justify-center"
      :class="[
        isSelected ? 'ring-4 ring-blue-500 ring-opacity-80' : 'hover:ring-2 hover:ring-gray-500 hover:ring-opacity-50',
        getSpriteClass() || 'bg-gray-700'
      ]"
    >
      <!-- Плейсхолдер з першою літерою назви (тільки якщо немає CSS класу спрайту) -->
      <span 
        v-if="!getSpriteClass()"
        class="text-gray-300 text-2xl font-bold"
      >
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

<style scoped>
/* CSS класи для спрайтів */

.bg-dark_fantasy_1 {
  width: 128px; 
  height: 128px;
  background: url('@/assets/style_sprites/sprite_test.png') -5px -5px;
  background-repeat: no-repeat;
}

.bg-temich {
  width: 128px; 
  height: 128px;
  background: url('@/assets/style_sprites/sprite_test.png') -143px -5px;
  background-repeat: no-repeat;
}

.bg-celestial {
  width: 128px; 
  height: 128px;
  background: url('@/assets/style_sprites/sprite_test.png') -143px -5px;
  background-repeat: no-repeat;
}

</style> 