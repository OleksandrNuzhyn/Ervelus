  <template>
    <div @click.stop class="relative cursor-default transition-all duration-200 ease-in-out transform hover:scale-105">
      <div 
        @click.stop="selectStyle"
        class="w-45 h-45 rounded-2xl mx-auto transition-all duration-200 flex items-center justify-center relative cursor-pointer"
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
      
      <div class="mt-3 text-center pointer-events-none">
        <span class="text-white text-sm font-medium">{{ styleData.name }}</span>
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
.bg-dark_fantasy {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/fantasy.png') -209px -10px;
  background-repeat: no-repeat;
}

.bg-light_fantasy {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/fantasy.png') -410px -10px;
  background-repeat: no-repeat;
}

.bg-gothic_fantasy {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/fantasy.png') -10px -210px;
  background-repeat: no-repeat;
}

.bg-grimdark_fantasy {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/fantasy.png') -210px -210px;
  background-repeat: no-repeat;
}

.bg-adventure_fantasy {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/fantasy.png') -10px -10px;
  background-repeat: no-repeat;
}


.bg-stone_age {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/time_travel.png') -410px -10px;
  background-repeat: no-repeat;
}

.bg-ancient_greece {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/time_travel.png') -10px -10px;
  background-repeat: no-repeat;
}

.bg-medieval_realism {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/time_travel.png') -210px -10px;
  background-repeat: no-repeat;
}

.bg-the_gilded_age {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/time_travel.png') -210px -210px;
  background-repeat: no-repeat;
}

.bg-wild_west {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/time_travel.png') -10px -210px;
  background-repeat: no-repeat;
}


.bg-wonders_of_giza {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/around_the_world.png') -410px -10px;
  background-repeat: no-repeat;
}

.bg-parisian_dream {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/around_the_world.png') -210px -10px;
  background-repeat: no-repeat;
}

.bg-pripyat_gloom {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/around_the_world.png') -10px -210px;
  background-repeat: no-repeat;
}

.bg-venice_canals {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/around_the_world.png') -210px -210px;
  background-repeat: no-repeat;
}

.bg-japanese_spring {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/around_the_world.png') -10px -10px;
  background-repeat: no-repeat;
}

.bg-steampunk {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/punkverse.png') -410px -10px;
  background-repeat: no-repeat;
}

.bg-cyberpunk {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/punkverse.png') -210px -10px;
  background-repeat: no-repeat;
}

.bg-atompunk {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/punkverse.png') -10px -10px;
  background-repeat: no-repeat;
}

.bg-solarpunk {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/punkverse.png') -210px -210px;
  background-repeat: no-repeat;
}

.bg-dieselpunk {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/punkverse.png') -10px -210px;
  background-repeat: no-repeat;
}

.bg-carnival_in_rio_de_janeiro {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/events.png') -10px -10px;
  background-repeat: no-repeat;
}

.bg-chinise_new_year {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/events.png') -210px -10px;
  background-repeat: no-repeat;
}

.bg-halloween {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/events.png') -10px -210px;
  background-repeat: no-repeat;
}

.bg-merry_christmas {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/events.png') -210px -210px;
  background-repeat: no-repeat;
}

.bg-valentines_day {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/events.png') -410px -10px;
  background-repeat: no-repeat;
}

.bg-dark_cinematic {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/trending.png') -10px -10px;
  background-repeat: no-repeat;
}

.bg-diplomatic_elevator {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/trending.png') -210px -10px;
  background-repeat: no-repeat;
}

.bg-hong_kong_urban {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/trending.png') -10px -210px;
  background-repeat: no-repeat;
}

.bg-tokyo_drive {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/trending.png') -210px -210px;
  background-repeat: no-repeat;
}

.bg-yacht_chillin {
  width: 180px; 
  height: 180px;
  background: url('@/assets/style_sprites/trending.png') -410px -10px;
  background-repeat: no-repeat;
}
</style>