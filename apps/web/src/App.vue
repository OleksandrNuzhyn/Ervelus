<template>
  <div id="app" class="min-h-screen text-white">
    <router-view />
    <Transition name="fade" @after-enter="onLoaderFadedIn">
      <div v-if="isLoading" class="loader-overlay"></div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoading = ref(false);
let resolveNavigation = null;

function onLoaderFadedIn() {
  if (resolveNavigation) {
    resolveNavigation();
    resolveNavigation = null;
  }
}

router.beforeEach(async (to, from) => {
  if (from.name === undefined) {
    return true;
  }

  isLoading.value = true;
  await new Promise((resolve) => {
    resolveNavigation = resolve;
  });

  return true;
});

router.afterEach(() => {
  isLoading.value = false;
});
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background-color: #0c0d14;
}
</style>