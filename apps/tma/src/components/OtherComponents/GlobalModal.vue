```
<template>
  <Transition name="modal-fade">
    <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-[110] modal-backdrop" @click.self="handleBackdropClick">
      <div 
        v-if="type === 'success'"
        class="solid-panel w-11/12 max-w-md min-h-[220px] flex flex-col items-center justify-between shadow-2xl transition-all overflow-hidden"
      >
          <div class="pointer-events-none absolute -left-10 -top-10 h-48 w-48 rounded-full bg-emerald-500/20 blur-[100px]"></div>
          <div class="pointer-events-none absolute -bottom-10 -right-10 h-48 w-48 rounded-full bg-green-500/20 blur-[100px]"></div>

          <div class="relative z-10 flex flex-col items-center w-full pt-10 pb-4 px-8 text-center">
            <h3 class="mb-3 text-2xl font-bold tracking-tight text-white">{{ title }}</h3>
            <p class="text-[15px] font-medium leading-relaxed text-white/50">
              {{ message }}
            </p>
          </div>

          <div class="w-full px-6 pb-7 pt-2 relative z-10 text-center">
            <button 
              @click="handleClose" 
              class="w-full bg-white/[0.08] hover:bg-white/[0.12] active:scale-[0.98] transition-all text-white font-bold rounded-xl py-3.5 text-[15px]"
            >
              {{ cancelText || $t('store.got_it') }}
            </button>
          </div>
      </div>
      
      <div 
        v-else-if="type === 'error'"
        class="solid-panel w-11/12 max-w-md min-h-[220px] flex flex-col items-center justify-between shadow-2xl transition-all overflow-hidden"
      >
          <div class="pointer-events-none absolute -left-10 -top-10 h-48 w-48 rounded-full bg-rose-500/20 blur-[100px]"></div>
          <div class="pointer-events-none absolute -bottom-10 -right-10 h-48 w-48 rounded-full bg-red-500/15 blur-[100px]"></div>

          <div class="relative z-10 flex flex-col items-center w-full pt-10 pb-4 px-8 text-center">
            <h3 class="mb-3 text-2xl font-bold tracking-tight text-white">{{ title }}</h3>
            <p class="text-[15px] font-medium leading-relaxed text-white/50">
              {{ message }}
            </p>
          </div>

          <div class="w-full px-6 pb-7 pt-2 relative z-10 text-center">
            <button 
              @click="handleClose" 
              class="w-full bg-white/[0.08] hover:bg-white/[0.12] active:scale-[0.98] transition-all text-white font-bold rounded-xl py-3.5 text-[15px]"
            >
              {{ cancelText || $t('profile.modal_got_it') }}
            </button>
          </div>
      </div>

      <div 
        v-else
        class="solid-panel w-11/12 max-w-md min-h-[220px] flex flex-col items-center justify-between text-gray-200 relative overflow-hidden"
      >
        <div class="pointer-events-none absolute -left-10 -top-10 h-48 w-48 rounded-full bg-white/10 blur-[100px]"></div>
        
        <div class="relative z-10 w-full pt-10 pb-4 px-8 text-center">
          <h3 class="text-2xl font-bold text-white tracking-wide mb-3">{{ title }}</h3>
          <p class="text-[15px] text-white/50 leading-relaxed font-medium">{{ message }}</p>
        </div>
        
        <div class="w-full px-6 pb-7 pt-2 relative z-10">
          <div v-if="onConfirm" class="flex flex-col gap-3 w-full">
             <button 
              @click="handleConfirm" 
              class="w-full bg-white/[0.08] hover:bg-white/[0.12] active:scale-[0.98] transition-all text-white font-bold rounded-xl py-3.5 text-[15px]"
            >
              {{ confirmText || $t('gallery.confirm') }}
            </button>
             <button 
              @click="handleCancel" 
              class="w-full bg-white/[0.04] hover:bg-white/[0.08] active:scale-[0.98] transition-all text-white/40 hover:text-white/60 font-bold rounded-xl py-3.5 text-[15px]"
            >
              {{ cancelText || $t('profile.modal_cancel') }}
            </button>
          </div>

          <div v-else class="w-full flex justify-center">
            <button 
              @click="handleClose" 
              class="w-full bg-white/[0.08] hover:bg-white/[0.12] active:scale-[0.98] transition-all text-white font-bold rounded-xl py-3.5 text-[15px]"
            >
              {{ cancelText || $t('profile.modal_got_it') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useModalStore } from '@/stores/modal';

const modalStore = useModalStore();
const { isOpen, title, message, type, confirmText, cancelText, onConfirm, onCancel } = storeToRefs(modalStore);

function handleClose() {
  modalStore.closeModal();
}

function handleBackdropClick() {
  if (!onConfirm.value) {
    handleClose();
  }
}

function handleConfirm() {
  if (onConfirm.value) {
    onConfirm.value();
  }
  handleClose();
}

function handleCancel() {
  if (onCancel.value) {
    onCancel.value();
  }
  handleClose();
}
</script>