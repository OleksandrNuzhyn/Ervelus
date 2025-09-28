<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-gray-950 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-50 overflow-y-auto">
        <div
          class="flex md:max-h-screen items-end justify-center p-4 text-center sm:items-center sm:p-0"
        >
          <TransitionChild
            as="template"
            enter="ease-out duration-300" 
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="flex flex-col transform overflow-hidden rounded-lg bg-zinc-950 border border-zinc-700 p-4 text-left shadow-2xl transition-all sm:my-8 w-[95vw] sm:max-w-7xl md:h-[95vh]"
              :class="{ 'h-[95vh]': isLoading }"
            >
              <div v-if="isLoading" class="flex flex-col items-center justify-center h-full">
                <p class="text-sm sm:text-base text-zinc-300/90">Loading high-quality images...</p>
              </div>

              <div v-else-if="duo" class="grid grid-cols-1 md:grid-cols-2 gap-4 h-full">
                <div class="flex flex-col items-center h-full">
                  <h3 class="text-lg font-medium text-white mb-2">Input Image</h3>
                  <div class="relative flex-grow flex items-center justify-center w-full bg-zinc-900 border border-zinc-700 md:hover:border-zinc-500 transition duration-300 rounded-lg">
                    <img
                      :src="duo.input_img_signed_url"
                      alt="Input Image"
                      class="object-contain w-full h-auto max-h-[80vh] rounded-lg "
                    />
                    <!-- <a
                      :href="duo.input_img_download_url"
                      download="input-image.png"
                      class="absolute bottom-0 right-0 mb-4 mr-4 h-min w-min inline-flex justify-center"
                    >
                      <FiDownload class="h-min w-min stroke-white md:stroke-zinc-500" />
                    </a> -->
                  </div>
                </div>

                <div class="flex flex-col items-center h-full">
                  <h3 class="text-lg font-medium text-white mb-2">Output Image</h3>
                  <div class="relative flex-grow flex items-center justify-center w-full bg-zinc-900 border border-zinc-700 md:hover:border-zinc-500 transition duration-300 rounded-lg">
                    <img
                      :src="duo.output_img_signed_url"
                      alt="Output Image"
                      class="object-contain w-full h-auto max-h-[80vh] rounded-lg"
                    />
                    <a
                      href="#"
                      @click.prevent="downloadImage(duo.id)"
                      class="absolute bottom-0 right-0 mb-4 mr-4 h-min w-min inline-flex justify-center"
                    >
                      <FiDownload class="h-min w-min stroke-white md:stroke-zinc-500" />
                    </a>
                  </div>
                </div>
              </div>

              <div v-if="!isLoading" class="mt-4 flex justify-between items-center">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-zinc-800 px-4 py-2 text-base font-medium text-red-400 shadow-sm hover:bg-zinc-700 sm:text-sm"
                  @click="$emit('delete-duo', duo.id)"
                >
                  Delete
                </button>
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-zinc-800 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-zinc-700 sm:text-sm"
                  @click="$emit('close-modal')"
                >
                  Close
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import FiDownload from '@/assets/fi_download.svg';
import api from '@/services/api'
import {
  Dialog,
  DialogPanel,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue';
import axios from 'axios';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  duo: {
    type: Object,
    default: null,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close-modal', 'delete-duo']);

const closeModal = () => {
  emit('close-modal');
};

const downloadImage = async (pk) => {
  try {
    const response = await api.get(`api/generations/generation-requests/download/${pk}/`)
    console.log(response.data)
    const url = response.data.download_url;
    const link = document.createElement('a');
    link.href = url;
    console.log(link.href)
    link.setAttribute('download', `image-${pk}.png`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Download failed:', error);
  }
};
</script>
