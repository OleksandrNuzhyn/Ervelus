    <template>
  <div class="relative">
    <div class="w-full">
      <div class="relative">
        <CategoryStrip :categories="genres" :selected-category-id="selectedGenreId" @category-selected="handleGenreSelect"/>
        <transition name="slide-fade">
          <StylePanel
            v-if="isStylePanelOpen"
            class="absolute top-full mt-3 w-64/65 left-1/2 -translate-x-1/2 z-20"
            :styles="filteredStyles"
            :selected-style-id="selectedStyleId"
            @style-selected="handleStyleSelect"
            @close="handleClosePanel" />
        </transition>
      </div>
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

const handleOpenStylePanel = () => {
    if (!selectedGenreId.value) {
      selectedGenreId.value = genres.value[0].id;
    }
    isStylePanelOpen.value = true;
};

</script>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-out;
}

.slide-fade-enter-from {
  transform: translateY(-100px);
  opacity: 0;
}
.slide-fade-leave-to {
  transform: translateY(-100px);
  opacity: 0;
}
</style>
