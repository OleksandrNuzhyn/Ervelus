<template>
  <div class="promo-wrapper">
    <button 
      @click="isExpanded = !isExpanded"
      class="promo-pill"
      :class="{ 'active': isExpanded }"
    >
      <div class="shimmer-effect"></div>
      <svg class="pill-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
      </svg>
      <span class="pill-text">{{ $t('promo.free_20') }}</span>
    </button>

    <Teleport to="body">
      <transition name="dropdown">
        <div v-if="isExpanded" class="promo-dropdown" @click.stop>
          <button @click="isExpanded = false" class="dropdown-close">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          
          <div class="dropdown-glow"></div>

          <div 
            ref="scrollContainer"
            @scroll="checkScroll"
            class="promo-scroll-container mask-fade-vertical"
            :style="{
              '--mask-top': canScrollUp ? '100px' : '0px',
              '--mask-bottom': canScrollDown ? '100px' : '0px'
            }"
          >
            <div class="promo-inner-content">
              <div class="dropdown-icon-wrapper">
                <svg class="dropdown-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                </svg>
              </div>
              
              <h3 class="dropdown-title">{{ $t('promo.title') }}</h3>
              
              <div class="dropdown-content">
                <p class="intro-text">{{ $t('promo.subtitle') }}</p>
                
                <ul class="steps-list">
                  <li>
                    <span class="step-number">1.</span>
                    <span class="step-text">
                      <i18n-t keypath="promo.step_1" scope="global">
                        <template #link>
                          <span class="url-highlight">ervelus.com</span>
                        </template>
                      </i18n-t>
                    </span>
                  </li>
                  <li>
                    <span class="step-number">2.</span>
                    <span class="step-text">
                      <i18n-t keypath="promo.step_2" scope="global">
                        <template #link>
                          <span class="url-highlight">{{ $t('promo.discord_link') }}</span>
                        </template>
                      </i18n-t>
                    </span>
                  </li>
                </ul>
              </div>
              
              <a 
                href="https://discord.gg/pRD6KjtS7E" 
                target="_blank" 
                rel="noopener noreferrer"
                class="discord-button"
                @click.stop
              >
                <svg class="button-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515a.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0a12.64 12.64 0 00-.617-1.25a.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057a19.9 19.9 0 005.993 3.03a.078.078 0 00.084-.028a14.09 14.09 0 001.226-1.994a.076.076 0 00-.041-.106a13.107 13.107 0 01-1.872-.892a.077.077 0 01-.008-.128a10.2 10.2 0 00.372-.292a.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127a12.299 12.299 0 01-1.873.892a.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028a19.839 19.839 0 006.002-3.03a.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.956-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.955-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.946 2.418-2.157 2.418z"/>
                </svg>
                {{ $t('promo.open_discord') }}
              </a>
            </div>
          </div>
        </div>
      </transition>

      <div 
        v-if="isExpanded" 
        @click="isExpanded = false"
        class="dropdown-overlay"
      ></div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

const isExpanded = ref(false);
const scrollContainer = ref(null);
const canScrollUp = ref(false);
const canScrollDown = ref(false);

function checkScroll() {
  const el = scrollContainer.value;
  if (!el) return;
  
  canScrollUp.value = el.scrollTop > 10;
  canScrollDown.value = el.scrollTop + el.clientHeight < el.scrollHeight - 10;
}

watch(isExpanded, (newVal) => {
  if (newVal) {
    nextTick(() => {
      checkScroll();
      setTimeout(checkScroll, 300);
    });
  }
});
</script>

<style scoped>
.promo-wrapper {
  position: relative;
}

.promo-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 24px;
  font-size: 14px;
  font-weight: 700;
  color: white;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 980px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

@media (max-width: 767px) {
  .promo-pill {
    padding: 6px 16px;
    font-size: 13px;
  }
}

.shimmer-effect {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.08),
    rgba(255, 255, 255, 0.25),
    rgba(255, 255, 255, 0.08),
    transparent
  );
  animation: shimmer 4s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  20% { left: 100%; }
  100% { left: 100%; }
}

.promo-pill:hover {
  background: rgba(255, 255, 255, 0.15);
}

.promo-pill.active {
  background: rgba(255, 255, 255, 0.22);
}

.pill-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.pill-text {
  white-space: nowrap;
  letter-spacing: 0.04em;
  font-size: 13px;
  text-shadow: none;
}

.promo-dropdown {
  position: fixed;
  top: 78px; 
  left: 18px;
  right: 18px;
  bottom: 12px;
  background: radial-gradient(circle at 20% 0%, rgba(139, 92, 246, 0.08), transparent 40%),
              radial-gradient(circle at 80% 100%, rgba(88, 101, 242, 0.05), transparent 40%),
              #0a0a0c;
  border: none;
  border-radius: 20px;
  box-shadow: 
    0 50px 100px rgba(0, 0, 0, 0.9),
    0 0 120px rgba(139, 92, 246, 0.12); 
  z-index: 1000;
  overflow: hidden;
  transition: opacity 0.4s ease;
  padding: 0 !important;
}

.promo-scroll-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 0;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.promo-scroll-container::-webkit-scrollbar {
  display: none;
}

.promo-inner-content {
  width: 100%;
  min-height: 100%;
  padding: 0 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
}

.promo-inner-content::before {
  content: '';
  flex-grow: 1;
  min-height: 40px;
  width: 100%;
}

.promo-inner-content::after {
  content: '';
  flex-grow: 1;
  min-height: 80px;
  width: 100%;
}

.mask-fade-vertical {
  mask-image: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0,0,0,0.4) calc(var(--mask-top, 0px) / 2),
    black var(--mask-top, 0px),
    black calc(100% - var(--mask-bottom, 0px)),
    rgba(0,0,0,0.4) calc(100% - (var(--mask-bottom, 0px) / 2)),
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0,0,0,0.4) calc(var(--mask-top, 0px) / 2),
    black var(--mask-top, 0px),
    black calc(100% - var(--mask-bottom, 0px)),
    rgba(0,0,0,0.4) calc(100% - (var(--mask-bottom, 0px) / 2)),
    transparent 100%
  );
  transition: mask-image 0.3s ease-in-out, -webkit-mask-image 0.3s ease-in-out;
}

@media (min-width: 1024px) {
  .promo-dropdown {
    top: 90px;
    left: 50%;
    right: auto;
    bottom: auto;
    width: 620px; 
    max-width: 95vw;
    transform: translateX(-50%);
    overflow: visible;
  }
  .promo-scroll-container {
    display: block;
    overflow-y: visible;
    mask-image: none !important;
    -webkit-mask-image: none !important;
  }
  .promo-inner-content {
    padding: 48px 32px 40px;
    display: block;
  }
  .promo-inner-content::before,
  .promo-inner-content::after {
    display: none;
  }
}

@media (max-height: 740px) and (max-width: 1023px) {
  .dropdown-icon-wrapper {
    margin-bottom: 20px;
  }
  .dropdown-title {
    margin-bottom: 24px;
    font-size: 24px;
  }
}

@media (max-height: 680px) and (max-width: 1023px) {
  .dropdown-icon-wrapper {
    display: none;
  }
  .dropdown-title {
    font-size: 22px;
    margin-bottom: 12px;
  }
}

.dropdown-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.05), transparent 70%);
  pointer-events: none;
  z-index: -1;
}

.dropdown-close {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
}

.dropdown-close:hover {
  color: white;
}

.dropdown-icon-wrapper {
  width: 72px;
  height: 72px;
  margin: 0 auto 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
}

.dropdown-icon {
  width: 40px;
  height: 40px;
  color: #fff;
  filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.5));
}

.dropdown-title {
  font-size: 28px;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.04em;
  color: white;
  margin: 0 0 48px 0;
  flex-shrink: 0;
}

.dropdown-content {
  text-align: left;
  max-width: 480px;
  margin: 0 auto 64px;
  width: 100%;
  flex-shrink: 0;
}

.intro-text {
  font-size: 17px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20px;
}

.steps-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.steps-list li {
  display: flex;
  gap: 12px;
  font-size: 16px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 16px;
}

.step-number {
  font-weight: 800;
  color: white;
  flex-shrink: 0;
}

.url-highlight {
  color: white;
  font-weight: 700;
}

.discord-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 18px 48px;
  font-size: 16px;
  font-weight: 700;
  color: #000;
  background: #fff;
  border: none;
  border-radius: 980px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
  white-space: nowrap;
  flex-shrink: 0;
  width: auto;
  min-width: fit-content;
}

.discord-button:hover {
  background: #fff;
  transform: scale(1.02);
  box-shadow: 0 0 60px rgba(255, 255, 255, 0.5);
}

.discord-button:active {
  transform: scale(0.98);
}

.button-icon {
  width: 20px;
  height: 20px;
}

.dropdown-overlay {
  position: fixed;
  inset: 0;
  z-index: 99;
  background: rgba(0, 0, 0, 0.7);
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@media (min-width: 1024px) {
  .dropdown-enter-from,
  .dropdown-leave-to {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px) scale(0.97);
  }
}

@media (max-width: 1023px) {
  .dropdown-enter-from,
  .dropdown-leave-to {
    opacity: 0;
    transform: translateY(-20px) scale(0.97);
  }
}
</style>