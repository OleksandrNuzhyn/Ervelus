<template>
  <section class="relative mx-auto max-w-7xl px-6 lg:pt-8 pb-3 lg:px-8 h-full flex flex-col ">
    <div id="gallery-top"></div>

    <div class="mt-6 flex-grow flex items-start justify-center ">
      <div v-if="loading" class="w-full flex items-center justify-center py-10">
        <p class="text-sm sm:text-base text-zinc-300/90" role="status" aria-live="polite">
          Loading your gallery…
        </p>
      </div>

      <div
        v-else-if="galleryItems.length"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full"
      >
        <article
          v-for="duo in galleryItems"
          :key="duo.id"
          class="group relative overflow-hidden rounded-2xl border border-white/10 bg-zinc-900/50 backdrop-blur shadow-2xl ring-1 ring-black/20 hover:border-white/20 transition cursor-pointer"
          @click="openModal(duo)"
        >
          <div class="relative p-3 sm:p-4">
            <div class="grid grid-cols-2 gap-2">
              <figure class="relative overflow-hidden rounded-xl ring-1 ring-white/10">
                <img
                  :src="duo.input_img_signed_url"
                  alt="Input Image"
                  loading="lazy"
                  class="h-full w-full object-cover aspect-square"
                />
              </figure>
              <figure class="relative overflow-hidden rounded-xl ring-1 ring-white/10">
                <img
                  :src="duo.output_img_signed_url"
                  alt="Output Image"
                  loading="lazy"
                  class="h-full w-full object-cover aspect-square"
                />
              </figure>
            </div>

            <div class="mt-3 flex items-center justify-between text-xs text-zinc-300/80 font-medium">
              <span>Input</span>
              <span>Output</span>
            </div>
          </div>

          <div
            class="pointer-events-none absolute inset-0 rounded-2xl ring-0 ring-emerald-400/0 group-hover:ring-2 group-hover:ring-emerald-400/30 transition"
            aria-hidden="true"
          />
        </article>
      </div>

      <div
        v-else
        class="mx-auto max-w-md text-center rounded-2xl border border-white/10 bg-zinc-900/40 backdrop-blur p-10 text-zinc-300"
      >
        <p class="text-lg font-medium">No items yet</p>
        <p class="mt-1 text-sm text-zinc-400">Generate your first pair to see it here.</p>
      </div>
    </div>

    <PaginationComponent
      v-if="pageCount > 1"
      :page="page"
      :page-count="pageCount"
      :loading="loading"
      class="select-none"
      @change="changePage"
    />

    <ImageModal
      :is-open="isModalOpen"
      :duo="selectedDuo"
      :is-loading="isModalLoading"
      @close-modal="closeModal"
      @delete-duo="deleteDuo"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import api from '@/services/api'
import PaginationComponent from '@/components/GalleryComponents/PaginationComponent.vue'
import ImageModal from '@/components/GalleryComponents/ImageModal.vue'

const galleryItems = ref([])
const loading = ref(true)

const page = ref(1)
const pageCount = ref(1)
const count = ref(0)

const isModalOpen = ref(false)
const selectedDuo = ref(null)
const isModalLoading = ref(false)

const customPageSize = 12

const preloadImages = (urls) => {
  const promises = urls.map(url => {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = resolve
      img.onerror = reject
      img.src = url
    })
  })
  return Promise.all(promises)
}

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

const openModal = async (duo) => {
  isModalOpen.value = true
  isModalLoading.value = true
  selectedDuo.value = null // Clear previous data
  
  try {
    // Fetch high-quality data
    const res = await api.get(`api/generations/generation-requests/retrieve/${duo.id}/`)
    const fullDuoData = res.data;

    // Preload high-quality images before showing the modal content
    const imageUrls = [fullDuoData.input_img_signed_url, fullDuoData.output_img_signed_url];
    await preloadImages(imageUrls);

    // Set the data and show the modal
    selectedDuo.value = fullDuoData;
  } catch (e) {
    console.error('Failed to load full image data:', e);
  } finally {
    isModalLoading.value = false;
  }
}

const closeModal = () => {
  isModalOpen.value = false
  selectedDuo.value = null
}

const deleteDuo = async (duoId) => {
  if (!confirm('Are you sure you want to delete this image pair?')) {
    return
  }

  try {
    await api.delete(`api/generations/generation-requests/delete/${duoId}/`)
    closeModal()
    await fetchPage(page.value)
  } catch (e) {
    console.error('Failed to delete image pair:', e)
  }
}

onMounted(() => fetchPage(1))

const changePage = async (p) => {
  if (p < 1 || p > pageCount.value || p === page.value) return
  await fetchPage(p)
  await nextTick()
  const el = document.getElementById('gallery-top')
  if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' })
}
</script>