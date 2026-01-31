<template>
  <div class="flex items-center w-full" :class="{'md:space-x-4': isScrollable}">
    <div v-if="isScrollable" class="hidden md:flex w-10 shrink-0 justify-end">
      <button v-show="showLeftArrow" @click="scrollLeft" class="p-2 rounded-full bg-black/20 hover:bg-black/40 text-gray-400 hover:text-white transition-all border border-white/[0.02]">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
      </button>
    </div>
    
    <div class="relative flex-grow bg-white/[0.03] backdrop-blur-[20px] border border-white/[0.02] shadow-xl rounded-2xl overflow-hidden">
      <div ref="scrollContainer" 
        class="py-2 px-4 md:py-3 overflow-x-auto no-scrollbar min-h-[52px] md:min-h-[60px] flex items-center scroll-smooth mask-fade"
        :style="{
          '--mask-left': showLeftArrow ? '64px' : '0px',
          '--mask-right': showArrow ? '64px' : '0px'
        }"
      >
        <div class="flex items-center space-x-2 md:space-x-12" :class="isScrollable ? 'justify-start' : 'justify-center w-full'">
          <button v-for="category in categories" :key="category.id" @click="selectCategory(category.id)" :class="['px-5 py-1.5 md:py-2.5 rounded-full text-[13px] font-semibold transition-all duration-300 flex-shrink-0 whitespace-nowrap inter', selectedCategoryId === category.id ? 'bg-white/20 text-white shadow-sm' : 'bg-transparent text-white/50 hover:text-white/80 hover:bg-white/5']">{{ category.name }}</button>
        </div>
      </div>
    </div>

    <div v-if="isScrollable" class="hidden md:flex w-10 shrink-0 justify-start">
      <button v-show="showArrow" @click="scrollRight" class="p-2 rounded-full bg-black/20 hover:bg-black/40 text-gray-400 hover:text-white transition-all border border-white/[0.02]">
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

    el.style.setProperty('--mask-left', showLeftArrow.value ? '60px' : '0px');
    el.style.setProperty('--mask-right', showArrow.value ? '60px' : '0px');
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

function scrollToSelected() {
  nextTick(() => {
    const el = scrollContainer.value;
    if (!el) return;
    
    const selectedBtn = el.querySelector('button.bg-white\\/20');
    if (selectedBtn) {
      const elCenter = el.clientWidth / 2;
      const btnCenter = selectedBtn.offsetLeft + (selectedBtn.clientWidth / 2);
      const targetPos = btnCenter - elCenter;
      
      el.scrollTo({
        left: targetPos,
        behavior: 'smooth'
      });
    }
  });
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
    scrollToSelected();
  });
  resizeObserver.observe(el);
  watch(() => props.categories, () => {
    nextTick(() => {
      checkScroll();
      scrollToSelected();
    });
  }, { deep: true, immediate: true });
  
  watch(() => props.selectedCategoryId, () => {
    scrollToSelected();
  });

  nextTick(() => {
    checkScroll();
    scrollToSelected();
  });
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

.mask-fade {
  mask-image: linear-gradient(
    to right,
    transparent 0%,
    black var(--mask-left, 0px),
    black calc(100% - var(--mask-right, 0px)),
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(
    to right,
    transparent 0%,
    black var(--mask-left, 0px),
    black calc(100% - var(--mask-right, 0px)),
    transparent 100%
  );
  transition: none;
}
</style>