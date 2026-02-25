<template>
  <div class="relative">
    <div class="relative mb-1">
      <CategoryStrip :categories="genres" :selected-category-id="selectedGenreId" :is-style-panel-open="modalStore.isStylePanelOpen" @category-selected="handleGenreSelect"/>
      <transition
        enter-active-class="transition-opacity duration-400 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-400 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="modalStore.isStylePanelOpen" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[58]" @click="handleClosePanel"></div>
      </transition>
      
      <transition
        enter-active-class="transition-all duration-400 ease-out"
        enter-from-class="opacity-0 translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-300 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-2"
      >
        <StylePanel
          v-if="modalStore.isStylePanelOpen"
          class="!absolute top-full mt-2 w-full left-0 z-[60] transform-gpu"
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
      ref="imageWorkspaceRef"
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
import { useModalStore } from '@/stores/modal';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const customPreloadImages = [
  spriteFantasy,
  spriteTimeTravel,
  spriteAroundTheWorld,
  spritePunkverse,
  spriteEvents,
  spriteTrending
];

const productsStore = useProductsStore();
const modalStore = useModalStore();
const { styles, genres } = storeToRefs(productsStore);
const selectedGenreId = ref(null);
const selectedStyleId = ref(null);
const latestGenerationData = ref(null);

watch(() => modalStore.isStylePanelOpen, (val) => {
  if (val) {
    window.scrollTo(0, 0);
    document.body.style.overflow = 'hidden';
  }
  else {
    document.body.style.overflow = '';
  }
});

onUnmounted(() => {
  document.body.style.overflow = '';
});

onMounted(async () => {
  try {
    customPreloadImages.forEach(src => {
      const img = new Image();
      img.src = src;
    });

    if (styles.value.length === 0) {
      await productsStore.getStyles();
      if (styles.value.length === 0) {
        throw new Error('Styles not loaded');
      }
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
  }
  catch (error) {
    modalStore.openModal({ title: t('workspace.error_title'), message: t('workspace.error_load_failed') });
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
  if (!modalStore.isStylePanelOpen) {
    modalStore.openStylePanel();
  }
}

function handleStyleSelect(styleId) {
  selectedStyleId.value = styleId;
  const selectedStyle = styles.value.find(s => s.id === styleId);
  if (selectedStyle && selectedStyle.genre) {
    selectedGenreId.value = selectedStyle.genre.name;
  }
  modalStore.closeStylePanel();
}

function handleClosePanel() {
  modalStore.closeStylePanel();
  const style = styles.value.find(s => s.id === selectedStyleId.value);
  if (style && style.genre) {
    selectedGenreId.value = style.genre.name;
  }
}

function handleOpenStylePanel() {
  modalStore.openStylePanel();
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