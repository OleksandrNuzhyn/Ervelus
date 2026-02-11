<template>
  <Transition name="modal-fade">
    <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-[110] modal-backdrop" @click.self="handleBackdropClick">
      <div 
        v-if="type === 'success'"
        class="glass-card w-11/12 max-w-sm overflow-hidden p-8 text-center backdrop-blur-xl shadow-2xl transition-all"
      >
          <div class="pointer-events-none absolute -left-10 -top-10 h-32 w-32 rounded-full bg-green-500/20 blur-3xl"></div>
          <div class="pointer-events-none absolute -bottom-10 -right-10 h-32 w-32 rounded-full bg-emerald-500/10 blur-3xl"></div>

          <div class="relative z-10 flex flex-col items-center">
            <div class="relative mb-6 flex h-20 w-20 items-center justify-center">
              <div class="absolute inset-0 rounded-full bg-green-500/20 blur-xl"></div>
              <div class="relative flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-tr from-green-500 to-emerald-600 shadow-lg shadow-emerald-500/30">
                <svg class="h-6 w-6 text-white drop-shadow-md" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>

            <h3 class="mb-3 text-2xl font-bold tracking-tight text-white">{{ title }}</h3>
            
            <p class="mb-8 text-[15px] font-medium leading-relaxed text-white/60 whitespace-nowrap">
              {{ message }}
            </p>

            <button 
              @click="handleClose" 
              class="group relative flex w-full items-center justify-center overflow-hidden rounded-xl bg-white text-[15px] font-bold text-black shadow-lg transition-transform active:scale-[0.98]"
            >
              <div class="absolute inset-0 bg-gradient-to-r from-gray-100 to-white opacity-100 transition-opacity group-hover:opacity-90"></div>
              <span class="relative py-3.5">{{ cancelText || $t('store.got_it') }}</span>
            </button>
          </div>
      </div>
      
      <div 
        v-else-if="type === 'error'"
        class="glass-card w-11/12 max-w-sm overflow-hidden p-8 text-center backdrop-blur-xl shadow-2xl transition-all"
      >
          <div class="pointer-events-none absolute -left-10 -top-10 h-32 w-32 rounded-full bg-amber-500/15 blur-3xl"></div>
          <div class="pointer-events-none absolute -bottom-10 -right-10 h-32 w-32 rounded-full bg-orange-500/10 blur-3xl"></div>

          <div class="relative z-10 flex flex-col items-center">
            <div class="relative mb-6 flex h-20 w-20 items-center justify-center">
              <div class="absolute inset-0 rounded-full bg-amber-500/15 blur-xl"></div>
              <div class="relative flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-tr from-amber-400 to-orange-500 shadow-lg shadow-amber-500/20">
                <svg class="h-6 w-6 text-white drop-shadow-md" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
            </div>

            <h3 class="mb-3 text-2xl font-bold tracking-tight text-white">{{ title }}</h3>
            
            <p class="mb-8 text-[15px] font-medium leading-relaxed text-white/60">
              {{ message }}
            </p>

            <button 
              @click="handleClose" 
              class="group relative flex w-full items-center justify-center overflow-hidden rounded-xl bg-white/10 border border-white/5 text-[15px] font-bold text-white shadow-lg transition-transform active:scale-[0.98] hover:bg-white/20"
            >
              <span class="relative py-3.5">{{ cancelText || $t('profile.modal_got_it') }}</span>
            </button>
          </div>
      </div>

      <div 
        v-else
        class="glass-card !p-10 w-11/12 max-w-md min-h-[220px] flex flex-col items-center justify-center gap-8 text-gray-200 relative"
      >
        <div class="text-center">
          <h3 class="text-xl font-bold text-gray-200 tracking-wide mb-2">{{ title }}</h3>
          <p class="text-[15px] text-white/50 leading-relaxed font-medium">{{ message }}</p>
        </div>
        
        <div v-if="onConfirm" class="flex flex-col sm:flex-row justify-center gap-3 pt-2 w-full">
           <button 
            @click="handleConfirm" 
            class="flex items-center justify-center h-[48px] min-w-[140px] px-6 text-[14px] font-bold rounded-2xl transition-all duration-300 bg-white/20 border border-white/[0.02] text-white hover:bg-white/30 active:scale-[0.98]"
          >
            {{ confirmText || $t('gallery.confirm') }}
          </button>
           <button 
            @click="handleCancel" 
            class="flex items-center justify-center h-[48px] min-w-[140px] px-6 text-[14px] font-bold rounded-2xl transition-all duration-300 bg-white/5 border border-white/[0.02] text-white/40 hover:bg-white/10 active:scale-[0.98]"
          >
            {{ cancelText || $t('profile.modal_cancel') }}
          </button>
        </div>

        <div v-else class="flex justify-center pt-2 w-full">
          <button 
            @click="handleClose" 
            class="flex items-center justify-center h-[48px] min-w-[160px] px-8 text-[14px] font-bold rounded-2xl transition-all duration-300 bg-white/20 border border-white/[0.02] text-white hover:bg-white/30 active:scale-[0.98]"
          >
            {{ cancelText || $t('profile.modal_got_it') }}
          </button>
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