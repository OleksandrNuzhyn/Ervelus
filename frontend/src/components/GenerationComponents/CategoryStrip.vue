<template>
  <div class="relative px-3">
    <div
      ref="scrollContainer"
      class="bg-black/30 backdrop-blur-[7px] shadow-[0_0_3px_rgba(0,0,0)] rounded-xl p-2 md:p-3 overflow-x-auto no-scrollbar min-h-[52px] md:min-h-[60px] flex items-center"
    >
      <div class="flex items-center space-x-4 md:space-x-6 whitespace-nowrap flex-nowrap px-2">
        <button
          v-for="category in categories"
          :key="category.id"
          @click="selectCategory(category.id)"
          :class="[
            'w-30 md:w-60 py-2 rounded-md text-sm md:text-md font-semibold transition-colors flex-shrink-0',
            selectedCategoryId === category.id
              ? 'bg-transparent text-white'
              : 'bg-transparent text-gray-400 hover:text-white',
          ]"
        >
          {{ category.name }}
        </button>
      </div>
    </div>
    <div
      v-if="showLeftArrow"
      class="absolute top-0 left-0 h-full w-16 flex items-center justify-start pointer-events-none bg-gradient-to-r from-black/80 to-transparent pl-4"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-8 w-8 text-white"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </div>
    <div
      v-if="showArrow"
      class="absolute top-0 right-0 h-full w-16 flex items-center justify-end pointer-events-none bg-gradient-to-l from-black/80 to-transparent pr-4"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-8 w-8 text-white"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  </div>
</template>



<script setup>
import { onMounted, ref, watch, nextTick} from 'vue';

const props = defineProps({
  categories: {
    type: Array,
    required: true,
  },
  selectedCategoryId: {
    type: [String, Number],
    required: false,
    default: null,
  },
});

const emit = defineEmits(['category-selected']);

const selectCategory = (categoryId) => {
  emit('category-selected', categoryId);
};

const scrollContainer = ref(null);
const showArrow = ref(false);
const showLeftArrow = ref(false);

const checkScroll = () => {
  const el = scrollContainer.value;
  if (el) {
    const isScrollable = el.scrollWidth > el.clientWidth;
    const isScrolledToEnd = el.scrollLeft + el.clientWidth >= el.scrollWidth - 1;
    showArrow.value = isScrollable && !isScrolledToEnd;
    showLeftArrow.value = isScrollable && el.scrollLeft > 0;
  }
};

onMounted(() => {
  const elemento = scrollContainer.value;
  if (!elemento) return;

  elemento.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
      e.preventDefault();
      elemento.scrollLeft += e.deltaY;
    }
  }, { passive: false });

  elemento.addEventListener('scroll', checkScroll);
  window.addEventListener('resize', checkScroll);

  watch(
    () => props.categories,
    () => {
      nextTick(() => {
        checkScroll();
      });
    },
    { deep: true, immediate: true }
  );
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