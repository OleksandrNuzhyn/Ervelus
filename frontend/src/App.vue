<template>
  <div id="app" class="min-h-screen text-white">
    <router-view v-if="authStore.authChecked" />

    <Transition name="fade" @after-enter="onLoaderFadedIn">
      <div v-if="isLoading || !authStore.authChecked" class="loader-overlay">
        <div class="stars"></div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
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

.stars {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background-image:
    radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
    radial-gradient(1.5px 1.5px at 50px 160px, #ddd, rgba(0,0,0,0)),
    radial-gradient(2.5px 2.5px at 90px 40px, #fff, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 100px 100px, #eee, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 250px 250px;
  animation: animateStarLayer1 800s linear infinite;
}

.stars::before,
.stars::after {
  content: '';
  position: absolute;
  inset: 0;
}

.stars::before {
  background-image:
    radial-gradient(2px 2px at 10px 200px, #ddd, rgba(0,0,0,0)),
    radial-gradient(2.5px 2.5px at 150px 150px, #fff, rgba(0,0,0,0)),
    radial-gradient(3px 3px at 200px 30px, #eee, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 10px 200px, #ddd, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 350px 350px;
  animation: animateStarLayer2 1000s linear infinite;
}

.stars::after {
  background-image:
    radial-gradient(3px 3px at 80px 80px, #fff, rgba(0,0,0,0)),
    radial-gradient(4px 4px at 120px 20px, #eee, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 450px 450px;
  animation: animateStarLayer3 1300s linear infinite;
}

@keyframes animateStarLayer1 {
  from { background-position: 0 0; }
  to { background-position: 10000px 10000px; }
}

@keyframes animateStarLayer2 {
  from { background-position: 0 0; }
  to { background-position: -10000px 10000px; }
}

@keyframes animateStarLayer3 {
  from { background-position: 0 0; }
  to { background-position: 10000px -10000px; }
}
</style>
