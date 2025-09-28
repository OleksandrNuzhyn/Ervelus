<template>
  <!-- Fill the available height provided by the page container -->
  <section class="relative mx-auto max-w-7xl px-6 lg:pt-8 pb-3 lg:px-8 h-full flex flex-col ">
    <!-- (Optional anchor) -->
    <div id="gallery-top"></div>

    <!-- Main content area expands; no page scroll -->
    <div class="mt-6 flex-grow flex items-start justify-center ">
      <!-- Loading skeletons -->
      <!-- Loading (text only) -->
        <div
          v-if="loading"
          class="w-full flex items-center justify-center py-10"
        >
          <p class="text-sm sm:text-base text-zinc-300/90" role="status" aria-live="polite">
            Loading your gallery…
          </p>
        </div>


      <!-- Cards -->
      <div
        v-else-if="galleryItems.length"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full"
      >
        <article
          v-for="duo in galleryItems"
          :key="duo.id"
          class="group relative overflow-hidden rounded-2xl border border-white/10 bg-zinc-900/50 backdrop-blur shadow-2xl ring-1 ring-black/20 hover:border-white/20 transition"
        >
          <div class="relative p-3 sm:p-4">
            <!-- Grid of images -->
            <div class="grid grid-cols-2 gap-2">
              <!-- Input -->
              <figure class="relative overflow-hidden rounded-xl ring-1 ring-white/10">
                <img
                  :src="duo.input_img_signed_url"
                  alt="Input Image"
                  loading="lazy"
                  class="h-full w-full object-cover aspect-square"
                />
                <!-- Buttons -->
                <div
                  class="absolute w-full px-1 items-end justify-between bottom-1 hidden sm:flex gap-2 opacity-0 group-hover:opacity-100 transition"
                >
                  <button
                    class="px-3 py-1.5 rounded-md text-xs bg-black/60 text-white ring-1 ring-white/15 hover:bg-black/75"
                    @click="open(duo.input_img_signed_url)"
                  >
                    View
                  </button>
                  <!-- <button
                    class="p-1.5 rounded-md bg-black/60 text-white ring-1 ring-white/15 hover:bg-black/75 flex items-center justify-center"
                    @click="download(duo.input_img_signed_url, `${duo.id}-input`)"
                    aria-label="Download input"
                    title="Download"
                  >
                    <ArrowDownTrayIcon class="h-4 w-4" />
                  </button> -->
                </div>
              </figure>

              <!-- Output -->
              <figure class="relative overflow-hidden rounded-xl ring-1 ring-white/10">
                <img
                  :src="duo.output_img_signed_url"
                  alt="Output Image"
                  loading="lazy"
                  class="h-full w-full object-cover aspect-square"
                />
                <!-- Buttons -->
                <div
                  class="absolute w-full px-1 items-end justify-between bottom-1 hidden sm:flex gap-2 opacity-0 group-hover:opacity-100 transition"
                >
                  <button
                    class="px-3 py-1.5 rounded-md text-xs bg-black/60 text-white ring-1 ring-white/15 hover:bg-black/75"
                    @click="open(duo.output_img_signed_url)"
                  >
                    View
                  </button>
                  <!-- <button
                    class="p-1.5 rounded-md bg-black/60 text-white ring-1 ring-white/15 hover:bg-black/75 flex items-center justify-center"
                    @click="download(duo.output_img_signed_url, `${duo.id}-output`)"
                    aria-label="Download output"
                    title="Download"
                  >
                    <ArrowDownTrayIcon class="h-4 w-4" />
                  </button> -->
                </div>
              </figure>
            </div>

            <!-- Footer labels -->
            <div class="mt-3 flex items-center justify-between text-xs text-zinc-300/80 font-medium">
              <span>Input</span>
              <span>Output</span>
            </div>
          </div>

          <!-- Hover accent -->
          <div
            class="pointer-events-none absolute inset-0 rounded-2xl ring-0 ring-emerald-400/0 group-hover:ring-2 group-hover:ring-emerald-400/30 transition"
            aria-hidden="true"
          />
        </article>
      </div>

      <!-- Empty -->
      <div
        v-else
        class="mx-auto max-w-md text-center rounded-2xl border border-white/10 bg-zinc-900/40 backdrop-blur p-10 text-zinc-300"
      >
        <p class="text-lg font-medium">No items yet</p>
        <p class="mt-1 text-sm text-zinc-400">Generate your first pair to see it here.</p>
      </div>
    </div>

    <!-- Pagination pinned to the bottom by flex layout -->
    <PaginationComponent
      v-if="pageCount > 1"
      :page="page"
      :page-count="pageCount"
      :loading="loading"
      class="select-none"
      @change="changePage"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import api from '@/services/api'
import { ArrowDownTrayIcon } from '@heroicons/vue/24/solid'
import PaginationComponent from '@/components/GalleryComponents/PaginationComponent.vue'

const galleryItems = ref([])
const loading = ref(true)

const page = ref(1)
const pageCount = ref(1)
const count = ref(0)

const customPageSize = 12

const fetchPage = async (p = 1) => {
  loading.value = true
  try {
    const res = await api.get(
      `api/generations/generation-requests/gallery/?custom_page_size=${customPageSize}&page=${p}`
    )
    const data = res.data || {}
    galleryItems.value = data.results || []
    count.value = Number(data.count || 0)
    page.value = p
    pageCount.value = Math.max(1, Math.ceil(count.value / customPageSize))
  } catch (e) {
    console.error('Failed to load gallery:', e)
    galleryItems.value = []
    count.value = 0
    page.value = 1
    pageCount.value = 1
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchPage(1))

const changePage = async (p) => {
  if (p < 1 || p > pageCount.value || p === page.value) return
  await fetchPage(p)
  await nextTick()
  // no page scroll overall, but we can still ensure focus shift if needed
  const el = document.getElementById('gallery-top')
  if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' })
}

const open = (url) => window.open(url, '_blank', 'noopener,noreferrer')

const download = async (url, name = 'image') => {
  const res = await fetch(url)
  const blob = await res.blob()
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  const mime = res.headers.get('Content-Type') || ''
  const ext = mime.includes('png') ? 'png' : mime.includes('webp') ? 'webp' : 'jpg'
  a.download = `${name}.${ext}`
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(a.href)
}

// kept if you re-add timestamps later
const formatTime = (d) => {
  if (!d) return ''
  try {
    return new Intl.DateTimeFormat(undefined, {
      dateStyle: 'medium',
      timeStyle: 'short'
    }).format(new Date(d))
  } catch {
    return ''
  }
}
</script>
