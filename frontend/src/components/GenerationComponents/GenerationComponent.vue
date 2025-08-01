  <template>
    <div class="relative">
      <div class="sticky top-6 z-50 w-full px-3">
        <div class="relative">
          <CategoryStrip :categories="mockCategories" :selected-category-id="selectedCategoryId" @category-selected="handleCategorySelect"/>
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
      <ImageWorkspace v-if="!isStylePanelOpen" :selected-style-name="selectedStyleName" />
    </div>
  </template>
  
  
<script setup>
import { ref, computed } from 'vue';
import CategoryStrip from './CategoryStrip.vue';
import StylePanel from './StylePanel.vue';
import ImageWorkspace from './ImageWorkspace.vue';

const mockCategories = [
  { id: 'anime', name: 'Аніме' },
  { id: 'photo', name: 'Фотореалізм' },
  { id: 'fantasy', name: 'Фентезі' },
  { id: 'cyberpunk', name: 'Кіберпанк' },
  { id: 'sci-fi', name: 'Наукова фантастика' },
  { id: 'abstract', name: 'Абстракція' },
  { id: 'realistic', name: 'Реалістичне' },
];

const mockStyles = [
  { id: 'anime_1', name: '80-ті', previewUrl: 'https://picsum.photos/seed/anime1/200', categoryId: 'anime', isPro: false },
  { id: 'anime_2', name: 'Ghibli', previewUrl: 'https://picsum.photos/seed/anime2/200', categoryId: 'anime', isPro: true },
  { id: 'photo_1', name: 'Портрет', previewUrl: 'https://picsum.photos/seed/photo1/200', categoryId: 'photo', isPro: false },
  { id: 'fantasy_1', name: 'Ельфійський ліс', previewUrl: 'https://picsum.photos/seed/fantasy1/200', categoryId: 'fantasy', isPro: false },
  { id: 'cyberpunk_1', name: 'Нео-Токіо', previewUrl: 'https://picsum.photos/seed/cyberpunk1/200', categoryId: 'cyberpunk', isPro: true },
];

const selectedCategoryId = ref('anime');
const selectedStyleId = ref(null);
const isStylePanelOpen = ref(false);

const filteredStyles = computed(() => mockStyles.filter(s=>s.categoryId===selectedCategoryId.value));

const selectedStyleName = computed(() => {
  const sel = mockStyles.find((s) => s.id === selectedStyleId.value);
  return sel ? sel.name : null;
});

const handleCategorySelect=(categoryId)=>{
  selectedCategoryId.value=categoryId;
  selectedStyleId.value=null;
  isStylePanelOpen.value=true;
};
const handleStyleSelect=(styleId)=>{
  selectedStyleId.value=styleId;
  isStylePanelOpen.value=false;
};
const handleClosePanel=()=>{
  isStylePanelOpen.value=false;
};

</script>
