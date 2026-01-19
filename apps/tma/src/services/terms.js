import { ref } from 'vue';

export const showTermsModal = ref(false);
export const requiredAgreements = ref([]);

export function show(agreements) {
  if (showTermsModal.value) {
    return;
  }
  requiredAgreements.value = agreements;
  showTermsModal.value = true;
}

export function hide() {
  showTermsModal.value = false;
  requiredAgreements.value = [];
}