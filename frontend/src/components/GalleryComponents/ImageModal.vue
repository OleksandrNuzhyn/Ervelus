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
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-50 overflow-y-auto">
        <div
          class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
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
              class="relative transform overflow-hidden rounded-lg bg-zinc-900 border border-white/10 p-4 text-left shadow-xl transition-all sm:my-8 w-full sm:max-w-4xl"
            >
              <div v-if="isLoading" class="flex flex-col items-center justify-center p-10">
                <p class="text-sm sm:text-base text-zinc-300/90">Loading high-quality images…</p>
              </div>

              <div v-else-if="duo" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="flex flex-col items-center">
                  <h3 class="text-lg font-medium text-white mb-2">Input Image</h3>
                  <img
                    :src="duo.input_img_signed_url"
                    alt="Input Image"
                    class="rounded-lg object-contain w-full h-auto max-h-[80vh] border border-white/10"
                  />
                </div>
                <div class="flex flex-col items-center">
                  <h3 class="text-lg font-medium text-white mb-2">Output Image</h3>
                  <img
                    :src="duo.output_img_signed_url"
                    alt="Output Image"
                    class="rounded-lg object-contain w-full h-auto max-h-[80vh] border border-white/10"
                  />
                </div>
              </div>

              <div class="mt-4 flex justify-between items-center">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 sm:text-sm"
                  @click="$emit('delete-duo', duo.id)"
                >
                  Delete
                </button>
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-zinc-700 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 sm:text-sm"
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
import {
  Dialog,
  DialogPanel,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'

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
})

const emit = defineEmits(['close-modal', 'delete-duo'])

const closeModal = () => {
  emit('close-modal')
}
</script>