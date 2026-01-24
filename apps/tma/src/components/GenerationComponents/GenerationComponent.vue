<template>
  <div class="relative">
    <div class="relative mb-1">
      <CategoryStrip :categories="genres" :selected-category-id="selectedGenreId" @category-selected="handleGenreSelect"/>
      <transition name="slide-fade">
        <StylePanel
          v-if="isStylePanelOpen"
          class="absolute top-full mt-2 w-full left-0 z-20"
          :styles="filteredStyles"
          :selected-style-id="selectedStyleId"
          :current-genre-name="selectedGenreId"
          @style-selected="handleStyleSelect"
          @next-genre="handleNextGenre"
          @prev-genre="handlePrevGenre"
          @close="handleClosePanel" />
      </transition>
    </div>
    <ImageWorkspace 
      v-show="!isStylePanelOpen" 
      :selected-style-name="selectedStyleName" 
      :selected-style-id="selectedStyleId" 
      :on-open-style-panel="handleOpenStylePanel"
      :latest-generation-data="latestGenerationData"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CategoryStrip from './CategoryStrip.vue';
import StylePanel from './StylePanel.vue';
import ImageWorkspace from './ImageWorkspace.vue';
import api from '@/services/api';

const genres = ref([]);
const styles = ref([]);

const selectedGenreId = ref(null);
const selectedStyleId = ref(null);
const isStylePanelOpen = ref(false);
const latestGenerationData = ref(null);

onMounted(async () => {
  const [stylesResponse, latestGenerationResponse] = await Promise.all([
    api.get('/api/products/styles/'),
    api.get('/api/generations/generation-requests/latest/')
  ]);

  styles.value = stylesResponse.data;
  latestGenerationData.value = latestGenerationResponse.data;

  if (styles.value.length > 0) {
    const genreMap = new Map();
    styles.value.forEach(style => {
      if (style.genre && style.genre.name && !genreMap.has(style.genre.name)) {
        genreMap.set(style.genre.name, { id: style.genre.name, name: style.genre.name });
      }
    });
    genres.value = Array.from(genreMap.values());
  }

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
    const parisianDreamStyle = styles.value.find(s => s.name.toLowerCase() === 'parisian dream');
    
    if (parisianDreamStyle) {
      selectedStyleId.value = parisianDreamStyle.id;
      if (parisianDreamStyle.genre && parisianDreamStyle.genre.name) {
        selectedGenreId.value = parisianDreamStyle.genre.name;
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
  return styles.value.filter(s => s.genre && s.genre.name === selectedGenreId.value);
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
.slide-fade-enter-active {
  transition: opacity 0.4s ease-in-out;
}

.slide-fade-enter-from {
  opacity: 0.5;
}
</style>