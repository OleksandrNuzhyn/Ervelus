  <template>
    <div
      @click="selectStyle"
      class="relative cursor-pointer transition-all duration-200 ease-in-out transform hover:scale-105"
    >
      <div 
        class="w-45 h-45 rounded-2xl mx-auto transition-all duration-200 flex items-center justify-center relative"
        :class="[
          isSelected ? 'ring-3 ring-gray-400' : 'hover:ring-2 hover:ring-gray-800 hover:ring-opacity-30',
          getSpriteClass() || 'bg-transparent'
        ]"
      >
  
        <div 
          v-if="styleData.is_available === false"
          class="absolute inset-0 flex items-center justify-center rounded-2xl">
          <div class="absolute inset-0 h-full w-full rounded-2xl bg-black opacity-50"></div>
          <svg class="w-8 h-8 text-white drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
          </svg>
        </div>
      </div>
      
      <div class="mt-3 text-center">
        <span class="text-white text-sm font-semibold">{{ styleData.name }}</span>
      </div>
      
    </div>
  </template>
  
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

function selectStyle() {
  if (props.styleData.is_available !== false) {
    emit('select-style', props.styleData.id);
  }
}

function getSpriteClass() {
  if (props.styleData.name) {
    const className = props.styleData.name
      .toLowerCase()
      .replace(/\s+/g, '_')
      .replace(/[^a-z0-9_]/g, '');
    const cssClass = `bg-${className}`;

    return cssClass;
  }
  return '';
}
</script>

<style scoped>
.bg-dark_fantasy_1 {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/sprite_test.png') -10px -10px;
  background-repeat: no-repeat;
}

.bg-temich {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/sprite_test.png') -210px -10px;
  background-repeat: no-repeat;
}

.bg-celestial {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/sprite_test.png') -210px -10px;
  background-repeat: no-repeat;
}

.bg-ukraine {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/sprite_test.png') -10px -10px;
  background-repeat: no-repeat;
}

.bg-steampunk {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/sprite_test.png') -10px -10px;
  background-repeat: no-repeat;
}
</style>