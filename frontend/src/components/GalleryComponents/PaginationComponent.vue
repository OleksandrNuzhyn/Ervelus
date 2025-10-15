<template>
  <nav class="mt-6 mb-6 flex items-center justify-center gap-2 text-sm" aria-label="Pagination">
    <button
      :class="[
        'px-3 py-2 rounded-md border backdrop-blur disabled:opacity-40 disabled:cursor-not-allowed transition-colors duration-400 ease-in-out',
        hoveredPage === 'prev'
          ? 'border-white/20 bg-white/10 text-white'
          : 'border-white/10 bg-black/30'
      ]"
      :disabled="page <= 1 || isLoading"
      @click="$emit('change', page - 1)"
      @mouseover="hoveredPage = 'prev'"
      @mouseleave="hoveredPage = null"
    >
      Prev
    </button>

    <button
      v-for="p in pagesToShow"
      :key="p"
      class="px-3 py-2 rounded-md border transition-colors duration-400 ease-in-out"
      :class="[
        (p === hoveredPage || (hoveredPage === null && p === page))
          ? 'border-white/20 bg-white/10 text-white backdrop-blur'
          : 'border-white/10 bg-black/30 backdrop-blur'
      ]"
      @click="$emit('change', p)"
      :disabled="isLoading"
      @mouseover="hoveredPage = p"
      @mouseleave="hoveredPage = null"
    >
      {{ p }}
    </button>

    <button
      :class="[
        'px-3 py-2 rounded-md border backdrop-blur disabled:opacity-40 disabled:cursor-not-allowed transition-colors duration-400 ease-in-out',
        hoveredPage === 'next'
          ? 'border-white/20 bg-white/10 text-white'
          : 'border-white/10 bg-black/30'
      ]"
      :disabled="page >= pageCount || isLoading"
      @click="$emit('change', page + 1)"
      @mouseover="hoveredPage = 'next'"
      @mouseleave="hoveredPage = null"
    >
      Next
    </button>
  </nav>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  page: { type: Number, required: true },
  pageCount: { type: Number, required: true },
  isLoading: { type: Boolean, default: false }
})

const hoveredPage = ref(null)

const pagesToShow = computed(() => {
  const start = Math.max(1, props.page - 1)
  const end = Math.min(props.pageCount, props.page + 1)
  const list = []
  for (let p = start; p <= end; p++) list.push(p)
  if (!list.includes(1)) list.unshift(1)
  if (!list.includes(props.pageCount)) list.push(props.pageCount)
  return Array.from(new Set(list)).sort((a, b) => a - b)
})
</script>