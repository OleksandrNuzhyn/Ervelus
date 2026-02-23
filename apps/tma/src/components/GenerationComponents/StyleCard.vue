<template>
    <div @click.stop="selectStyle" class="relative cursor-default transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-103 w-fit mx-auto">
      <div 
        class="w-45 h-45 rounded-2xl mx-auto transition-all duration-200 flex items-center justify-center relative cursor-pointer overflow-hidden transform-gpu bg-[#2a2a2a]"
        :class="[
          isSelected ? 'ring-1 ring-white/20 shadow-[0_0_15px_rgba(255,255,255,0.1)]' : 'hover:ring-2 hover:ring-white/20 hover:ring-opacity-50'
        ]"
      >
        <div class="absolute inset-0 w-full h-full" :class="getSpriteClass()"></div>
  
        <div 
          v-if="styleData.is_available === false"
          class="absolute inset-0 z-10 overflow-hidden rounded-2xl"
        >
          <div class="absolute -inset-10 flex items-center justify-center bg-black/20" style="filter: blur(4px) grayscale(0.4);">
             <div :class="getSpriteClass()" class="scale-125"></div>
          </div>
          
          <div class="absolute inset-0 bg-black/40 pointer-events-none"></div>

          <div class="absolute inset-0 flex items-center justify-center z-20">
            <div class="relative px-3 py-1.5 bg-black/60 backdrop-blur-md border border-white/1 rounded-full flex items-center gap-1.5 shadow-xl">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 15" fill="currentColor" class="w-3.5 h-3.5 text-yellow-400" style="filter: drop-shadow(0px 0px 3px rgba(0,0,0,1));">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M6.63869 12.1902L3.50621 14.1092C3.18049 14.3087 2.75468 14.2064 2.55515 13.8807C2.45769 13.7216 2.42864 13.5299 2.47457 13.3491L2.95948 11.4405C3.13452 10.7515 3.60599 10.1756 4.24682 9.86791L7.6642 8.22716C7.82352 8.15067 7.89067 7.95951 7.81418 7.80019C7.75223 7.67116 7.61214 7.59896 7.47111 7.62338L3.66713 8.28194C2.89387 8.41581 2.1009 8.20228 1.49941 7.69823L0.297703 6.69116C0.00493565 6.44581 -0.0335059 6.00958 0.211842 5.71682C0.33117 5.57442 0.502766 5.48602 0.687982 5.47153L4.35956 5.18419C4.61895 5.16389 4.845 4.99974 4.94458 4.75937L6.36101 1.3402C6.5072 0.987302 6.91179 0.819734 7.26469 0.965925C7.43413 1.03612 7.56876 1.17075 7.63896 1.3402L9.05539 4.75937C9.15496 4.99974 9.38101 5.16389 9.6404 5.18419L13.3322 5.47311C13.713 5.50291 13.9975 5.83578 13.9677 6.2166C13.9534 6.39979 13.8667 6.56975 13.7269 6.68896L10.9114 9.08928C10.7131 9.25826 10.6267 9.52425 10.6876 9.77748L11.5532 13.3733C11.6426 13.7447 11.414 14.1182 11.0427 14.2076C10.8642 14.2506 10.676 14.2208 10.5195 14.1249L7.36128 12.1902C7.13956 12.0544 6.8604 12.0544 6.63869 12.1902Z" fill="currentColor"></path>
              </svg>
              <span class="text-[12px] font-medium text-white/90 tracking-wide leading-none pb-[1px]">Premium</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-3 text-center pointer-events-none">
        <span class="text-white text-sm font-medium">{{ styleData.name }}</span>
      </div>
      
    </div>
  </template>
  
<script setup>
import { useModalStore } from '@/stores/modal';
const modalStore = useModalStore();

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
  if (props.styleData.is_available === false) {
    modalStore.openStore();
  }
  else {
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