  <template>
    <div class="bg-black/30 backdrop-blur-[7px] shadow-[0_0_3px_rgba(0,0,0)] rounded-xl h-[calc(100vh-10rem)] flex flex-col">
      <div class="flex-shrink-0 z-10 px-4 pt-4">
        <div class="flex justify-between items-center mb-3">
          <h2 class="text-2xl font-bold text-white flex-grow text-center">Choose your destiny</h2>
          <button @click="handleClose" class="text-gray-400 hover:text-white bg-transparent p-2 transition-colors">
            <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      <div class="overflow-y-auto no-scrollbar flex-grow" id="masked-scroll-container">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 px-4 pb-4 pt-3">
          <StyleCard
            v-for="style in styles"
            :key="style.id"
            :style-data="style"
            :is-selected="style.id === selectedStyleId"
            @select-style="onStyleSelected"/>
        </div>
      </div>
    </div>
  </template>

<script setup>
import StyleCard from './StyleCard.vue';

defineProps({
  styles: {
    type: Array,
    required: true,
  },
  selectedStyleId: {
    type: String,
    required: false,
    default: null
  },
});

const emit = defineEmits(['style-selected','close']);

function onStyleSelected(styleId) {
  emit('style-selected', styleId);
}

function handleClose() {
  emit('close');
}
</script>

<style scoped>
#masked-scroll-container {
  -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 1%);
  mask-image: linear-gradient(to bottom, transparent 0%, black 1%);
}

.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>