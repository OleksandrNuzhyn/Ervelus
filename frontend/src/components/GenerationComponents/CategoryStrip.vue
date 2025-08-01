<template>
  <div class="relative">
    <div
      ref="scrollContainer"
      class="bg-transparent backdrop-blur-[14px] bg-[rgba(10,10,10,0.3)] rounded-xl p-3 shadow-lg overflow-x-auto no-scrollbar"
    >
      <div class="flex items-center space-x-6 whitespace-nowrap flex-nowrap px-2">
        <button
          v-for="category in categories"
          :key="category.id"
          @click="selectCategory(category.id)"
          :class="[
            'w-60 py-2 rounded-md text-md font-semibold transition-colors flex-shrink-0',
            selectedCategoryId === category.id
              ? 'bg-blue-600 text-white'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600',
          ]"
        >
          {{ category.name }}
        </button>
      </div>
    </div>
    <div
      v-if="showArrow"
      class="absolute top-0 right-0 h-full w-16 flex items-center justify-end pointer-events-none bg-gradient-to-l from-[rgba(10,10,10,0.8)] to-transparent pr-4"
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

<style scoped>
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style> 


<script setup>
import { onMounted, ref, watch, nextTick, defineProps, defineEmits } from 'vue';

const props = defineProps({
  categories: {
    type: Array,
    required: true,
  },
  selectedCategoryId: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(['category-selected']);

const selectCategory = (categoryId) => {
  emit('category-selected', categoryId);
};

const scrollContainer = ref(null);
const showArrow = ref(false);

const checkScroll = () => {
  const el = scrollContainer.value;
  if (el) {
    const isScrollable = el.scrollWidth > el.clientWidth;
    const isScrolledToEnd = el.scrollLeft + el.clientWidth >= el.scrollWidth - 1;
    showArrow.value = isScrollable && !isScrolledToEnd;
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
