<template>
  <section class="relative mx-auto max-w-[1370px] px-4 pt-8 pb-3 h-full flex flex-col">
    <div id="gallery-top"></div>
    
    <div class="flex-grow"
      :class="{
        'overflow-y-auto': galleryItems.length > 0,
        'flex items-center justify-center': !galleryItems.length
      }">
      <transition name="gallery-fade">
        <transition-group
          v-if="!isLoading && galleryItems.length"
          tag="div"
          name="gallery-list"
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full mt-6"
        >
          <article
            v-for="request in galleryItems"
            :key="request.id"
            :class="{'gallery-item-visible': request.requestLoaded}"
            class="group relative overflow-hidden rounded-2xl border border-white/10 bg-zinc-900/50 backdrop-blur shadow-lg ring-1 ring-black/20 hover:border-white/20 cursor-pointer gallery-item generation-card"
            @click="openModal(request)"
          >
            <div class="flex flex-col p-3 sm:p-4 h-full">
              <div class="grid grid-cols-2 gap-2 h-full">
                <figure class="relative overflow-hidden rounded-xl bg-zinc-900/50 z-20">
                  <img v-if="request.input_img_signed_url" :src="request.input_img_signed_url" alt="Input Image" :class="['h-full w-full object-cover aspect-square image-fade', { 'image-visible': request.requestLoaded }]"/>
                </figure>
                <figure class="relative overflow-hidden rounded-xl bg-zinc-900/50 z-20">
                  <img v-if="request.output_img_signed_url" :src="request.output_img_signed_url" alt="Output Image" :class="['h-full w-full object-cover aspect-square image-fade', { 'image-visible': request.requestLoaded }]"/>
                </figure>
              </div>
              <div class="mt-3 flex items-center justify-between text-xs text-zinc-300/80 font-medium">
                <span class="pl-1">Original</span>
                <span class="pr-1">Stylized</span>
              </div>
            </div>
            <div
              class="pointer-events-none absolute inset-0 rounded-2xl ring-0 ring-emerald-400/0 group-hover:ring-2 group-hover:ring-emerald-400/30 transition"
              aria-hidden="true"
            />
          </article>
        </transition-group>
        <div v-else-if="!isLoading && !galleryItems.length" class="w-full mx-auto max-w-md text-center rounded-2xl border border-white/10 bg-zinc-900/40 backdrop-blur p-10 text-zinc-300">
          <p class="text-lg font-medium">No images yet</p>
          <p class="mt-1 text-sm text-zinc-400">Stylize your first images to see it here</p>
          <router-link to="/dashboard" class="manage-button small-manage-button mt-8 mx-auto">
            Go to Dashboard
          </router-link>
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
      @delete-request="deleteRequest"
    />
    
    <transition name="modal-fade">
      <div v-if="showDeleteConfirmModal" class="fixed inset-0 flex items-center justify-center z-50 confirm-modal-overlay" @click.self="handleCancelDelete">
        <div class="modal-content-card p-4 sm:p-8 w-11/12 max-w-md shadow-lg flex flex-col gap-5 text-gray-200 relative">
          <div class="pb-2">
            <h3 class="medieval text-2xl text-center text-gray-100">Delete Images</h3>
          </div>
          <div class="text-center">
            <p class="text-gray-300 text-base m-0 leading-relaxed">Are you sure you want to delete this images? This action cannot be undone</p>
          </div>
          <div class="flex justify-center gap-4 pt-4">
            <button @click="handleConfirmDelete" class="manage-button small-manage-button">Confirm</button>
          </div>
        </div>
      </div>
    </transition>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import PaginationComponent from '@/components/GalleryComponents/PaginationComponent.vue'
import GenerationModal from '@/components/GalleryComponents/GenerationModal.vue'

const galleryItems = ref([])
const isLoading = ref(true)
const page = ref(1)
const pageCount = ref(1)
const count = ref(0)
const customPageSize = 12
const isOpen = ref(false)
const selectedRequest = ref(null)
const showDeleteConfirmModal = ref(false);
let deleteActionResolve = null;

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
  
  try {
    const response = await api.get(`/api/generations/generation-requests/gallery/?custom_page_size=${customPageSize}&page=${p}`)
    
    galleryItems.value = (response.data?.results || []).map(request => ({ ...request, requestLoaded: false }));
    count.value = Number(response.data?.count || 0)
    pageCount.value = Math.max(1, Math.ceil(count.value / customPageSize))

    if ((response.data?.results || []).length > 0) {
      const initialDelay = 75; 
      const staggerMs = 75;

      for (const [index, request] of galleryItems.value.entries()) {
        setTimeout(async () => {
          const urlsToLoad = [request.input_img_signed_url, request.output_img_signed_url].filter(Boolean);
          if (urlsToLoad.length > 0) {
            await preloadRequest(urlsToLoad);
            request.requestLoaded = true;
          }
          else {
            request.requestLoaded = true;
          }
        }, initialDelay + (index * staggerMs));
      }
    }
  }
  catch {
    galleryItems.value = []
    count.value = 0
    page.value = 1
    pageCount.value = 1
  }
  finally {
    isLoading.value = false;
  }
}

async function deleteRequest(request) {
  showDeleteConfirmModal.value = true;

  const confirmed = await new Promise(resolve => {
    deleteActionResolve = resolve;
  });

  if (confirmed) {
    try {
      closeModal();

      const itemIndex = galleryItems.value.findIndex(item => item.id === request.id);
      if (itemIndex !== -1) {
        galleryItems.value.splice(itemIndex, 1);
      }

      await api.delete(`/api/generations/generation-requests/delete/${request.id}/`);
        
      count.value--;
      pageCount.value = Math.max(1, Math.ceil(count.value / customPageSize));
        
      if (galleryItems.value.length === 0 && page.value > 1) {
        await changePage(page.value - 1);
      }
      else if (galleryItems.value.length === 0 && count.value > 0) {
        await getPage(page.value);
      }
    }
    catch {
      console.error('Failed to delete image pair:');
    }
    finally {
      deleteActionResolve = null;
    }
  }
}

function handleConfirmDelete() {
  if (deleteActionResolve) {
    deleteActionResolve(true);
    showDeleteConfirmModal.value = false;
  }
}

function handleCancelDelete() {
  if (deleteActionResolve) {
    deleteActionResolve(false);
    showDeleteConfirmModal.value = false;
  }
}

async function changePage(p) {
  if (p < 1 || p > pageCount.value || p === page.value) {
    return;
  }
  page.value = p;

  await getPage(p);

  const element = document.getElementById('gallery-top')
  if (element) {
    element.scrollIntoView({ behavior: 'instant', block: 'start' })
  }
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
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

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

.generation-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.15);
  opacity: 0;
  transition: opacity 0.2s linear;
  pointer-events: none;
  z-index: 1;
  border-radius: inherit;
}

.generation-card:hover::before {
  opacity: 1;
}

.gallery-fade-leave-active {
  transition: opacity 0.4s ease;
  will-change: opacity, transform;
  transform: translateZ(0);
}

.gallery-fade-leave-to {
  opacity: 0;
}

.medieval {
  font-family: 'MedievalSharp', cursive;
}

.font-sans {
  font-family: 'Inter', sans-serif;
}

.manage-button {
  display: inline-block;
  width: auto;
  min-width: 270px;
  text-align: center;
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: 9999px;
  padding: 0.9rem 2.25rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #9ca3af;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  cursor: pointer;
}

.manage-button:hover {
  background: rgba(129, 180, 253, 0.1);
  color: #81b4fd;
  border-color: rgba(129, 180, 253, 0.4);
}

.small-manage-button {
  min-width: 0;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.modal-fade-enter-from {
  opacity: 0;
  transform: translateY(20px) translateZ(0);
}

.modal-fade-leave-to {
  opacity: 0;
  transform: translateZ(0);
}

.modal-content-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  will-change: backdrop-filter, transform;
  transform: translateZ(0);
}

.confirm-modal-overlay {
  background-color: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(22px);
}
</style>