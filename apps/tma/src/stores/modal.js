import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useModalStore = defineStore('modal', () => {
    const isOpen = ref(false);
    const isStoreOpen = ref(false);
    const title = ref('');
    const message = ref('');
    const type = ref('error');
    const confirmText = ref('');
    const cancelText = ref('');
    const onConfirm = ref(null);
    const onCancel = ref(null);

    function openModal(options) {
        title.value = options.title;
        message.value = options.message;
        type.value = options.type || 'error';
        confirmText.value = options.confirmText || '';
        cancelText.value = options.cancelText || '';
        onConfirm.value = options.onConfirm || null;
        onCancel.value = options.onCancel || null;
        isOpen.value = true;
    }

    function closeModal() {
        isOpen.value = false;
    }

    function openStore() {
        isStoreOpen.value = true;
    }

    function closeStore() {
        isStoreOpen.value = false;
    }

    return {
        isOpen,
        isStoreOpen,
        title,
        message,
        type,
        confirmText,
        cancelText,
        onConfirm,
        onCancel,
        openModal,
        closeModal,
        openStore,
        closeStore
    };
});