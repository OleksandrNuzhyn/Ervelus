<template>
  <div id="app" class="min-h-screen text-white">
    <router-view v-if="authStore.user && !authStore.isMaintenanceMode" />
    
    <Transition name="fade" @after-enter="onLoaderFadedIn">
      <div v-if="isLoading || !authStore.user || authStore.isMaintenanceMode" class="loader-overlay">

        <div v-if="authStore.isMaintenanceMode" class="maintenance-content">
          <Transition name="fade-box" appear>
            <div class="maintenance-box">
              <h1>The site is under maintenance</h1>
              <p>We'll be back soon. We apologize for the inconvenience.</p>
              <p class="mt-4 text-sm text-gray-400">Please refresh the page periodically to check our status</p>
            </div>
          </Transition>
        </div>

        <div v-else class="loader-content">
          <img src="@/assets/svg/staff_logo.svg" class="wave-animation w-24 h-24" />
        </div>

      </div>
    </Transition>
    
    <TermsAcceptModal />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import TermsAcceptModal from '@/components/OtherComponents/TermsAcceptModal.vue';

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
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

.wave-animation {
  animation: wave 1s ease-in-out infinite alternate;
  filter: drop-shadow(0 0 15px rgba(129, 180, 253, 0.2));
}

@keyframes wave {
  from { transform: rotate(35deg); }
  to { transform: rotate(50deg); }
}

.maintenance-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  text-align: center;
  padding: 0 1rem;
}

.maintenance-box {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(5px);
  padding: 2.5rem 4rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.fade-box-enter-active {
  transition: opacity 0.6s ease-out;
  transition-delay: 0.2s;
}

.fade-box-enter-from {
  opacity: 0;
  transform: translateZ(0);
}
</style>