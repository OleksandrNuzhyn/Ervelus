<template>
  <nav
    class="mt-6 mb-6 flex items-center justify-center gap-2 text-sm"
    aria-label="Pagination"
  >
    <button
      class="px-3 py-2 rounded-md border border-white/10 bg-black/30 backdrop-blur hover:bg-black/50 disabled:opacity-40 disabled:cursor-not-allowed"
      :disabled="page <= 1 || loading"
      @click="$emit('change', page - 1)"
    >
      Prev
    </button>

    <button
      v-for="p in pagesToShow"
      :key="p"
      class="px-3 py-2 rounded-md border"
      :class="[
        p === page
          ? 'border-gray-300 bg-gray-300/10'
          : 'border-white/10 bg-black/30 hover:bg-black/50'
      ]"
      @click="$emit('change', p)"
      :disabled="loading"
    >
      {{ p }}
    </button>

    <button
      class="px-3 py-2 rounded-md border border-white/10 bg-black/30 backdrop-blur hover:bg-black/50 disabled:opacity-40 disabled:cursor-not-allowed"
      :disabled="page >= pageCount || loading"
      @click="$emit('change', page + 1)"
    >
      Next
    </button>
  </nav>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  page: { type: Number, required: true },
  pageCount: { type: Number, required: true },
  loading: { type: Boolean, default: false },
  range: { type: Number, default: 1 },
})

const pagesToShow = computed(() => {
  const start = Math.max(1, props.page - props.range)
  const end = Math.min(props.pageCount, props.page + props.range)
  const list = []
  for (let p = start; p <= end; p++) list.push(p)
  if (!list.includes(1)) list.unshift(1)
  if (!list.includes(props.pageCount)) list.push(props.pageCount)
  return Array.from(new Set(list)).sort((a, b) => a - b)
})
</script>
