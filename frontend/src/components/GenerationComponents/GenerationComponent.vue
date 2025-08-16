<template>
  <div class="relative">
    <div class="w-full">
      <div class="relative">
        <CategoryStrip :categories="genres" :selected-category-id="selectedGenreId" @category-selected="handleGenreSelect"/>
        <StylePanel
          v-if="isStylePanelOpen"
          class="absolute top-full mt-2 w-full z-20"
          :styles="filteredStyles"
          :selected-style-id="selectedStyleId"
          @style-selected="handleStyleSelect"
          @close="handleClosePanel"
        />
      </div>
    </div>
    <ImageWorkspace v-show="!isStylePanelOpen" :selected-style-name="selectedStyleName" :selected-style-id="selectedStyleId" />
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

onMounted(async () => {
  try {
    const stylesResponse = await api.get('/api/products/styles/');
    styles.value = stylesResponse.data;

    if (styles.value.length > 0) {
      const genreMap = new Map();
      styles.value.forEach(style => {
        if (style.genre && style.genre.name && !genreMap.has(style.genre.name)) {
          genreMap.set(style.genre.name, { id: style.genre.name, name: style.genre.name });
        }
      });
      genres.value = Array.from(genreMap.values());

      if (genres.value.length > 0) {
        //selectedGenreId.value = genres.value[0].id;
        //isStylePanelOpen.value = true;
        //future: open most popular styles at begining
      }
    }
  } catch (error) {
    console.error('Failed to load style data:', error);
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

const handleGenreSelect=(genreId)=>{
  selectedGenreId.value = genreId;
  isStylePanelOpen.value = true;
};
const handleStyleSelect=(styleId)=>{
  selectedStyleId.value=styleId;
  isStylePanelOpen.value=false;
};
const handleClosePanel=()=>{
  isStylePanelOpen.value=false;
  selectedGenreId.value=null;
};

</script>
