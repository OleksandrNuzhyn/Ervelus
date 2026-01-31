<template>
  <div class="bg-white/[0.03] backdrop-blur-[20px] border border-white/[0.02] shadow-xl rounded-2xl h-[calc(100vh-10rem)] lg:h-[calc(100vh-10.6rem)] flex flex-col p-4 relative">
    <div class="relative w-full h-full flex flex-col min-h-0">
      <button @click="handleClose" class="absolute right-0 top-0 text-white/60 hover:text-white bg-transparent p-2 transition-colors z-30">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <div class="flex-shrink-0 z-10 w-full mb-3">
        <div class="flex items-center justify-center min-h-[44px]">
          <h2 class="text-xl font-medium text-white tracking-wide inter leading-none">{{ $t('workspace.choose_style') }}</h2>
        </div>
      </div>

      <div class="md:hidden absolute left-0 top-1/2 -translate-y-1/2 z-20 flex items-center">
        <button @click="$emit('prev-genre')" class="text-white/60 hover:text-white bg-transparent p-2 transition-colors active:scale-95">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        </button>
      </div>
      <div class="md:hidden absolute right-0 top-1/2 -translate-y-1/2 z-20 flex items-center">
        <button @click="$emit('next-genre')" class="text-white/60 hover:text-white bg-transparent p-2 transition-colors active:scale-95">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </button>
      </div>
      <div class="relative flex-grow min-h-0 group">
        <div 
          ref="scrollContainer"
          @scroll="checkScroll"
          class="w-full h-full overflow-y-auto no-scrollbar mask-fade-vertical" 
          id="masked-scroll-container"
          :style="{
            '--mask-top': '60px',
            '--mask-bottom': '60px'
          }"
        >
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 pb-6 lg:pb-8 pt-4 px-4">
            <StyleCard
              v-for="style in styles"
              :key="style.id"
              :style-data="style"
              :is-selected="style.id === selectedStyleId"
              @select-style="onStyleSelected"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import StyleCard from './StyleCard.vue';

const props = defineProps({
  styles: {
    type: Array,
    required: true,
  },
  selectedStyleId: {
    type: [String, Number],
    required: false,
    default: null
  },
  currentGenreName: {
    type: String,
    required: false,
    default: ''
  }
});

const emit = defineEmits(['style-selected', 'close', 'next-genre', 'prev-genre']);

const scrollContainer = ref(null);
const canScrollUp = ref(true);
const canScrollDown = ref(true);

function checkScroll() {
  const el = scrollContainer.value;
  if (!el) return;
  
  canScrollUp.value = el.scrollTop > 10;
  canScrollDown.value = el.scrollTop + el.clientHeight < el.scrollHeight - 10;
}

function onStyleSelected(styleId) {
  emit('style-selected', styleId);
}

function handleClose() {
  emit('close');
}

onMounted(() => {
  nextTick(() => {
    checkScroll();
    setTimeout(checkScroll, 500);
  });
});

watch(() => props.currentGenreName, () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = 0;
  }
});
</script>

<style scoped>
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.mask-fade-vertical {
  mask-image: linear-gradient(
    to bottom,
    rgba(0,0,0,0.2) 0%,
    rgba(0,0,0,0.6) calc(var(--mask-top, 0px) / 2),
    black var(--mask-top, 0px),
    black calc(100% - var(--mask-bottom, 0px)),
    rgba(0,0,0,0.6) calc(100% - (var(--mask-bottom, 0px) / 2)),
    rgba(0,0,0,0.2) 100%
  );
  -webkit-mask-image: linear-gradient(
    to bottom,
    rgba(0,0,0,0.2) 0%,
    rgba(0,0,0,0.6) calc(var(--mask-top, 0px) / 2),
    black var(--mask-top, 0px),
    black calc(100% - var(--mask-bottom, 0px)),
    rgba(0,0,0,0.6) calc(100% - (var(--mask-bottom, 0px) / 2)),
    rgba(0,0,0,0.2) 100%
  );
  transition: mask-image 0.5s ease-in-out, -webkit-mask-image 0.5s ease-in-out;
}
</style>