<template>
  <div class="flex items-center w-full" :class="{'md:space-x-4': isScrollable}">
    <div v-if="isScrollable" class="hidden md:flex w-10 shrink-0 justify-end">
      <button v-show="showLeftArrow" @click="scrollLeft" class="p-2 rounded-full bg-black/20 hover:bg-black/40 text-gray-400 hover:text-white transition-all border border-white/5">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
      </button>
    </div>
    
    <div class="relative flex-grow bg-black/30 backdrop-blur-[7px] shadow-[0_0_3px_rgba(0,0,0)] rounded-xl overflow-hidden">
      <div v-show="showLeftArrow" class="absolute left-0 top-0 bottom-0 w-16 bg-gradient-to-r from-black/60 to-transparent z-10 pointer-events-none transition-opacity duration-300"></div>
      <div v-show="showArrow" class="absolute right-0 top-0 bottom-0 w-16 bg-gradient-to-l from-black/60 to-transparent z-10 pointer-events-none transition-opacity duration-300"></div>

      <div ref="scrollContainer" 
        class="py-2 px-4 md:py-3 overflow-x-auto no-scrollbar min-h-[52px] md:min-h-[60px] flex items-center scroll-smooth"
        :style="{
          'mask-image': `linear-gradient(to right, 
            ${showLeftArrow ? 'transparent' : 'black'} 0%, 
            black ${showLeftArrow ? '64px' : '0px'}, 
            black ${showArrow ? 'calc(100% - 64px)' : '100%'}, 
            ${showArrow ? 'transparent' : 'black'} 100%)`,
          '-webkit-mask-image': `linear-gradient(to right, 
            ${showLeftArrow ? 'transparent' : 'black'} 0%, 
            black ${showLeftArrow ? '64px' : '0px'}, 
            black ${showArrow ? 'calc(100% - 64px)' : '100%'}, 
            ${showArrow ? 'transparent' : 'black'} 100%)`
        }"
      >
        <div class="flex items-center space-x-2 md:space-x-12" :class="isScrollable ? 'justify-start' : 'justify-center w-full'">
          <button v-for="category in categories" :key="category.id" @click="selectCategory(category.id)" :class="['px-4 py-1.5 md:py-2 rounded-full text-sm font-medium transition-all duration-200 flex-shrink-0 whitespace-nowrap', selectedCategoryId === category.id ? 'bg-white/10 text-white' : 'bg-transparent text-white/70 hover:text-white/90 hover:bg-white/5']">{{ category.name }}</button>
        </div>
      </div>
    </div>

    <div v-if="isScrollable" class="hidden md:flex w-10 shrink-0 justify-start">
      <button v-show="showArrow" @click="scrollRight" class="p-2 rounded-full bg-black/20 hover:bg-black/40 text-gray-400 hover:text-white transition-all border border-white/5">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, nextTick, onBeforeUnmount } from 'vue';

const props = defineProps({
  categories: { type: Array, required: true },
  selectedCategoryId: { type: [String, Number], required: false, default: null },
});

const emit = defineEmits(['category-selected']);

function selectCategory(categoryId) {
  emit('category-selected', categoryId);
}

const scrollContainer = ref(null);
const isScrollable = ref(false);
const showArrow = ref(false);
const showLeftArrow = ref(false);

function checkScroll() {
  const el = scrollContainer.value;
  if (el) {
    const scrollPossible = el.scrollWidth > el.clientWidth + 2;
    isScrollable.value = scrollPossible;
    showArrow.value = scrollPossible && (el.scrollLeft + el.clientWidth < el.scrollWidth - 2);
    showLeftArrow.value = scrollPossible && el.scrollLeft > 2;
  }
}

function scrollLeft() {
  const el = scrollContainer.value;
  if (el) {
    const scrollAmount = el.clientWidth * 0.7;
    el.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
  }
}

function scrollRight() {
  const el = scrollContainer.value;
  if (el) {
    const scrollAmount = el.clientWidth * 0.7;
    el.scrollBy({ left: scrollAmount, behavior: 'smooth' });
  }
}

let resizeObserver = null;

onMounted(() => {
  const el = scrollContainer.value;
  if (!el) return;
  el.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
      el.scrollLeft += e.deltaY;
      e.preventDefault();
    }
  }, { passive: false });
  el.addEventListener('scroll', () => {
    window.requestAnimationFrame(checkScroll);
  });
  resizeObserver = new ResizeObserver(() => {
    checkScroll();
  });
  resizeObserver.observe(el);
  watch(() => props.categories, () => {
    nextTick(checkScroll);
  }, { deep: true, immediate: true });
  nextTick(checkScroll);
});

onBeforeUnmount(() => {
  if (resizeObserver) resizeObserver.disconnect();
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
</style>