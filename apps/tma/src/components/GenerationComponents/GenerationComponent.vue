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
    <transition name="modal-fade">
      <div v-if="showErrorModal" class="fixed inset-0 flex items-center justify-center z-[150] confirm-modal-overlay" @click.self="showErrorModal = false">
        <div class="profile-card !bg-white/[0.08] !backdrop-blur-[30px] !p-10 w-11/12 max-w-md min-h-[220px] flex flex-col items-center justify-center gap-8 text-gray-200 relative">
          <div class="text-center">
            <h3 class="text-xl font-bold text-gray-200 tracking-wide mb-2">{{ errorModalTitle }}</h3>
            <p class="text-[15px] text-white/50 leading-relaxed font-medium">{{ errorModalMessage }}</p>
          </div>
          <div class="flex justify-center pt-2 w-full">
            <button 
              @click="showErrorModal = false" 
              class="flex items-center justify-center h-[48px] min-w-[160px] px-8 text-[14px] font-bold rounded-2xl transition-all duration-300 bg-white/20 border border-white/[0.02] text-white hover:bg-white/30 active:scale-[0.98]"
            >
              {{ $t('workspace.got_it') }}
            </button>
          </div>
        </div>
      </div>
    </transition>
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
import { useI18n } from 'vue-i18n';

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

const { t } = useI18n();
const showErrorModal = ref(false);
const errorModalTitle = ref('');
const errorModalMessage = ref('');

function openErrorModal(title, message) {
  errorModalTitle.value = title;
  errorModalMessage.value = message;
  showErrorModal.value = true;
}

watch(isStylePanelOpen, (val) => {
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

function handleOpenStore() {
  imageWorkspaceRef.value?.openStore();
}

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
    openErrorModal(t('workspace.error_title'), t('workspace.error_load_failed'));
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

.confirm-modal-overlay {
  background-color: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(22px);
}

.profile-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.02);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
  border-radius: 16px;
  padding: 2.5rem;
  position: relative;
  display: flex;
  flex-direction: column;
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.modal-fade-enter-from {
  opacity: 0;
  transform: translateY(20px) translateZ(0);
}

.modal-fade-leave-to {
  opacity: 0;
  transform: translateZ(0);
}
</style>