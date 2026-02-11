<template>
  <section class="relative mx-auto max-w-[1370px] pb-3 min-h-full flex flex-col">
    <div id="gallery-top"></div>
    
    <div class="flex-grow mb-2"
      :class="{
        'flex items-center justify-center': !isLoading && !galleryItems.length
      }">
      <transition-group
        v-if="!isLoading && galleryItems.length"
        tag="div"
        name="gallery-list"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-11/12 mx-auto pt-4"
      >
        <article
          v-for="request in galleryItems"
          :key="request.id"
          :class="{'gallery-item-visible': request.requestLoaded}"
          class="group relative rounded-2xl border border-white/[0.02] bg-white/[0.03] backdrop-blur-[25px] ring-1 ring-black/20 cursor-pointer gallery-item generation-card transition-all duration-300 shadow-xl"
          @click="openModal(request)"
        >
          <div class="flex flex-col p-3 sm:p-4 h-full">
            <div class="grid grid-cols-2 gap-2 h-full">
              <figure class="relative overflow-hidden rounded-2xl bg-zinc-900/50 z-20">
                <img v-if="request.input_thumb_signed_url" :src="request.input_thumb_signed_url" alt="Input Image" :class="['h-full w-full object-cover aspect-square image-fade', { 'image-visible': request.requestLoaded }]"/>
                <div v-else class="h-full w-full flex items-center justify-center bg-white/[0.02] backdrop-blur-sm">
                  <svg class="w-13 h-11 text-white/20" fill="none" viewBox="0 0 24 24" stroke="currentColor" preserveAspectRatio="none">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </figure>
              <figure class="relative overflow-hidden rounded-2xl bg-zinc-900/50 z-20">
                <img v-if="request.output_thumb_signed_url" :src="request.output_thumb_signed_url" alt="Output Image" :class="['h-full w-full object-cover aspect-square image-fade', { 'image-visible': request.requestLoaded }]"/>
                <div v-else class="h-full w-full flex items-center justify-center bg-white/[0.02] backdrop-blur-sm">
                  <svg class="w-13 h-11 text-white/20" fill="none" viewBox="0 0 24 24" stroke="currentColor" preserveAspectRatio="none">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </figure>
            </div>
            <div class="mt-3 flex items-center justify-between text-xs text-zinc-300/80 font-medium">
              <span class="pl-1">{{ $t('gallery.original') }}</span>
              <span class="pr-1">{{ $t('gallery.stylized') }}</span>
            </div>
          </div>
        </article>
      </transition-group>
      
      <transition name="gallery-fade">
        <div v-if="!isLoading && !galleryItems.length" class="w-11/12 max-w-2xl mx-auto pt-3">
          <div class="glass-card p-10 flex flex-col items-center justify-center gap-6 text-center">
            <div class="space-y-2">
              <h3 class="text-xl font-bold text-gray-200 tracking-wide">{{ $t('gallery.no_images') }}</h3>
              <p class="text-[15px] text-white/50 leading-relaxed font-medium mx-auto">{{ $t('gallery.no_images_desc') }}</p>
            </div>
            <div class="flex justify-center pt-2 w-full">
              <router-link to="/" class="flex items-center justify-center h-[48px] min-w-[200px] px-8 text-[14px] font-bold rounded-2xl transition-all duration-300 bg-white/[0.03] border border-white/[0.02] text-white hover:bg-white/10 active:scale-[0.98] no-underline">
                {{ $t('gallery.go_dashboard') }}
              </router-link>
            </div>
          </div>
        </div>
      </transition>
    </div>
    
    <div class="flex-shrink-0 py-5">
      <transition name="pagination-fade">
        <PaginationComponent
          v-if="pageCount > 1"
          :page="page"
          :page-count="pageCount"
          :is-loading="isLoading"
          class="select-none"
          @change="changePage"
        />
      </transition>
    </div>
    
    <GenerationModal
      :is-open="isOpen"
      :selected-request="selectedRequest"
      @close-modal="closeModal"
      @delete-request="confirmDeleteRequest"
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import PaginationComponent from '@/components/GalleryComponents/PaginationComponent.vue'
import GenerationModal from '@/components/GalleryComponents/GenerationModal.vue'
import { useModalStore } from '@/stores/modal';
import { useI18n } from 'vue-i18n';

const galleryItems = ref([])
const isLoading = ref(true)
const page = ref(1)
const pageCount = ref(1)
const count = ref(0)
const customPageSize = 12
const isOpen = ref(false)
const selectedRequest = ref(null)
const modalStore = useModalStore();
const { t } = useI18n();

async function preloadRequest(urlsToLoad) {
  const promises = urlsToLoad.map(urlToLoad => {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = resolve
      img.onerror = reject
      img.src = urlToLoad
    })
  })
  await Promise.all(promises)
}

async function getPage(p) {
  isLoading.value = true
  galleryItems.value = [];
  
  try {
    const response = await api.get(`/api/generations/generation-requests/gallery/?custom_page_size=${customPageSize}&page=${p}`)
    
    const results = response.data?.results || [];
    count.value = Number(response.data?.count || 0)
    pageCount.value = Math.max(1, Math.ceil(count.value / customPageSize))

    isLoading.value = false;

    if (results.length > 0) {
      const tempItems = results.map(request => ({ ...request, requestLoaded: false }));
      galleryItems.value = tempItems;
      
      animateGalleryItems(galleryItems.value);
    }
  }
  catch {
    galleryItems.value = []
    count.value = 0
    page.value = 1
    pageCount.value = 1
    isLoading.value = false;
    modalStore.openModal({ title: t('gallery.delete_title'), message: t('gallery.error_load') });
  }
}

async function animateGalleryItems(items) {
  const staggerMs = 75;
  for (const request of items) {
    const urlsToLoad = [request.input_thumb_signed_url, request.output_thumb_signed_url].filter(Boolean);
    if (urlsToLoad.length > 0) {
      await preloadRequest(urlsToLoad);
    }
    request.requestLoaded = true;
    await new Promise(resolve => setTimeout(resolve, staggerMs));
  }
}

function confirmDeleteRequest(request) {
  modalStore.openModal({
    title: t('gallery.delete_title'),
    message: t('gallery.delete_confirm'),
    type: 'info',
    confirmText: t('gallery.confirm'),
    cancelText: t('profile.modal_cancel'),
    onConfirm: () => deleteRequestItem(request)
  });
}

async function deleteRequestItem(request) {
  try {
    closeModal();
    const itemIndex = galleryItems.value.findIndex(item => item.id === request.id);
    if (itemIndex !== -1) {
      galleryItems.value.splice(itemIndex, 1);
    }

    await api.delete(`/api/generations/generation-requests/delete/${request.id}/`);
    modalStore.openModal({title: t('gallery.delete_title'), message: t('gallery.success_delete'), type: 'success'});
      
    count.value--;
    pageCount.value = Math.max(1, Math.ceil(count.value / customPageSize));
      
    if (galleryItems.value.length === 0 && page.value > 1) {
      await changePage(page.value - 1);
    }
    else if (galleryItems.value.length === 0 && count.value > 0) {
      await getPage(page.value);
    }
  }
  catch (error) {
    let message = t('gallery.error_delete');
    if (error.response?.status === 404) {
      message = t('gallery.error_not_found');
    }
    modalStore.openModal({ title: t('gallery.delete_title'), message });
  }
}

async function changePage(p) {
  if (p < 1 || p > pageCount.value || p === page.value) {
    return;
  }
  page.value = p;

  await getPage(p);

  window.scrollTo({ top: 0, behavior: 'instant' });
}

function openModal(request) {
  selectedRequest.value = request
  isOpen.value = true
}

function closeModal() {
  selectedRequest.value = null
  isOpen.value = false
}

onMounted(() => {
  getPage(1);
});
</script>

<style scoped>
.gallery-item {
  opacity: 0;
  transform: translateZ(0);
  will-change: opacity, transform;
  transition: opacity 0.8s ease-out;
}

.gallery-item-visible {
  opacity: 1;
}

.gallery-list-enter-active,
.gallery-list-leave-active {
  transition: opacity 0.5s ease;
  will-change: opacity, transform;
  transform: translateZ(0);
}

.gallery-list-enter-from,
.gallery-list-leave-to {
  opacity: 0;
}

.gallery-list-leave-active {
  position: absolute;
}

.image-fade {
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}

.image-visible {
  opacity: 1;
}

.pagination-fade-enter-active {
  transition: opacity 1s ease-in-out;
  will-change: opacity, transform;
  transform: translateZ(0);
}

.pagination-fade-enter-from {
  opacity: 0;
  transform: translateZ(0);
}

.gallery-fade-leave-active {
  transition: opacity 0.4s ease;
  will-change: opacity, transform;
  transform: translateZ(0);
}

.gallery-fade-leave-to {
  opacity: 0;
}

.gallery-fade-enter-active {
  transition: opacity 0.8s ease;
  will-change: opacity, transform;
  transform: translateZ(0);
}

.gallery-fade-enter-from {
  opacity: 0;
}

.manage-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  width: auto;
  min-width: 270px;
  text-align: center;
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: 9999px;
  padding: 0.9rem 2.25rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.02);
  color: #9ca3af;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  cursor: pointer;
}

.manage-button:not(:disabled):hover {
  background: rgba(129, 180, 253, 0.1);
  color: #81b4fd;
  border-color: rgba(129, 180, 253, 0.4);
  box-shadow: 0 0 15px rgba(129, 180, 253, 0.15);
}

.small-manage-button {
  min-width: 0;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}
</style>