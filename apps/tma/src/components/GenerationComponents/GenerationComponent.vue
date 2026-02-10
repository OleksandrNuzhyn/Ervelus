<template>
  <div class="relative">
    <div class="relative mb-1">
      <CategoryStrip :categories="genres" :selected-category-id="selectedGenreId" :is-style-panel-open="isStylePanelOpen" @category-selected="handleGenreSelect"/>
      <transition name="slide-fade">
        <StylePanel
          v-if="isStylePanelOpen"
          class="!absolute top-full mt-3 w-full left-0 z-[60]"
          :styles="filteredStyles"
          :selected-style-id="selectedStyleId"
          :current-genre-name="selectedGenreId"
          @style-selected="handleStyleSelect"
          @next-genre="handleNextGenre"
          @prev-genre="handlePrevGenre"
          @close="handleClosePanel" 
          @open-store="handleOpenStore" />
      </transition>
    </div>
    <ImageWorkspace 
      ref="imageWorkspaceRef"
      v-show="!isStylePanelOpen" 
      :selected-style-name="selectedStyleName" 
      :selected-style-id="selectedStyleId" 
      :on-open-style-panel="handleOpenStylePanel"
      :latest-generation-data="latestGenerationData"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue';
import CategoryStrip from './CategoryStrip.vue';
import StylePanel from './StylePanel.vue';
import ImageWorkspace from './ImageWorkspace.vue';
import api from '@/services/api';
import spriteFantasy from '@/assets/style_sprites/fantasy.png';
import spriteTimeTravel from '@/assets/style_sprites/time_travel.png';
import spriteAroundTheWorld from '@/assets/style_sprites/around_the_world.png';
import spritePunkverse from '@/assets/style_sprites/punkverse.png';
import spriteEvents from '@/assets/style_sprites/events.png';
import spriteTrending from '@/assets/style_sprites/trending.png';
import { useProductsStore } from '@/stores/products';
import { storeToRefs } from 'pinia';

const customPreloadImages = [
  spriteFantasy,
  spriteTimeTravel,
  spriteAroundTheWorld,
  spritePunkverse,
  spriteEvents,
  spriteTrending
];

const productsStore = useProductsStore();
const { styles, genres } = storeToRefs(productsStore);
const selectedGenreId = ref(null);
const selectedStyleId = ref(null);
const isStylePanelOpen = ref(false);
const latestGenerationData = ref(null);
const imageWorkspaceRef = ref(null);

const closeStylePanel = () => {
  isStylePanelOpen.value = false;
};

watch(isStylePanelOpen, (val) => {
  const tg = window.Telegram?.WebApp;
  if (val) {
    window.scrollTo(0, 0);
    document.body.style.overflow = 'hidden';
    tg?.BackButton.show();
    tg?.BackButton.onClick(closeStylePanel);
  }
  else {
    document.body.style.overflow = '';
    tg?.BackButton.offClick(closeStylePanel);
    tg?.BackButton.hide();
  }
});

onUnmounted(() => {
  const tg = window.Telegram?.WebApp;
  document.body.style.overflow = '';
  tg?.BackButton.offClick(closeStylePanel);
});

function handleOpenStore() {
  imageWorkspaceRef.value?.openStore();
}

onMounted(async () => {
  customPreloadImages.forEach(src => {
    const img = new Image();
    img.src = src;
  });

  if (styles.value.length === 0) {
    await productsStore.getStyles();
  }

  const latestGenerationResponse = await api.get('/api/generations/generation-requests/latest/');
  latestGenerationData.value = latestGenerationResponse.data;

  if (latestGenerationData.value && latestGenerationData.value.chosen_style) {
    const styleId = latestGenerationData.value.chosen_style;
    const selectedStyle = styles.value.find(s => s.id === styleId);
    if (selectedStyle) {
      selectedStyleId.value = styleId;
      if (selectedStyle.genre && selectedStyle.genre.name) {
        selectedGenreId.value = selectedStyle.genre.name;
      }
    }
  }
  else if (styles.value.length > 0) {
    const defaultStyle = styles.value.find(s => s.name.toLowerCase() === 'hong kong urban');
    
    if (defaultStyle) {
      selectedStyleId.value = defaultStyle.id;
      if (defaultStyle.genre && defaultStyle.genre.name) {
        selectedGenreId.value = defaultStyle.genre.name;
      }
    }
    else {
      const randomIndex = Math.floor(Math.random() * styles.value.length);
      const randomStyle = styles.value[randomIndex];
      selectedStyleId.value = randomStyle.id;
      if (randomStyle.genre && randomStyle.genre.name) {
        selectedGenreId.value = randomStyle.genre.name;
      }
    }
  }
});

const filteredStyles = computed(() => {
  if (!selectedGenreId.value) {
    return [];
  }
  const filtered = styles.value.filter(s => s.genre && s.genre.name === selectedGenreId.value);
  return filtered.sort((a, b) => {
    if (a.is_available === b.is_available) return 0;
    return a.is_available ? -1 : 1;
  });
});

const selectedStyleName = computed(() => {
  const sel = styles.value.find((s) => s.id === selectedStyleId.value);
  return sel ? sel.name : null;
});

function handleGenreSelect(genreId) {
  selectedGenreId.value = genreId;
  isStylePanelOpen.value = true;
}

function handleStyleSelect(styleId) {
  selectedStyleId.value = styleId;
  const selectedStyle = styles.value.find(s => s.id === styleId);
  if (selectedStyle && selectedStyle.genre) {
    selectedGenreId.value = selectedStyle.genre.name;
  }
  isStylePanelOpen.value = false;
}

function handleClosePanel() {
  isStylePanelOpen.value = false;
  const style = styles.value.find(s => s.id === selectedStyleId.value);
  if (style && style.genre) {
    selectedGenreId.value = style.genre.name;
  }
}

function handleOpenStylePanel() {
  isStylePanelOpen.value = true;
}

function handleNextGenre() {
  if (genres.value.length === 0) return;
  const currentIndex = genres.value.findIndex(g => g.id === selectedGenreId.value);
  const nextIndex = (currentIndex + 1) % genres.value.length;
  selectedGenreId.value = genres.value[nextIndex].id;
}

function handlePrevGenre() {
  if (genres.value.length === 0) return;
  const currentIndex = genres.value.findIndex(g => g.id === selectedGenreId.value);
  const prevIndex = (currentIndex - 1 + genres.value.length) % genres.value.length;
  selectedGenreId.value = genres.value[prevIndex].id;
}
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
}
</style>