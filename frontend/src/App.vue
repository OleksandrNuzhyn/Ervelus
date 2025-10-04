<template>
  <div id="app" class="min-h-screen text-white">
    <Transition name="fade">
      <div v-if="!authStore.authChecked" class="loader-container">
        <div class="stars"></div>
        <svg class="sigil" width="120" height="120" viewBox="0 0 100 100">
          <circle class="sigil-circle" cx="50" cy="50" r="45" />
          <path class="sigil-lines" d="M 50 15 V 35" />
          <path class="sigil-lines" d="M 50 85 V 65" />
          <path class="sigil-lines" d="M 15 50 H 35" />
          <path class="sigil-lines" d="M 85 50 H 65" />
          <path class="sigil-lines" d="M 27 27 L 41 41" />
          <path class="sigil-lines" d="M 73 73 L 59 59" />
          <path class="sigil-lines" d="M 27 73 L 41 59" />
          <path class="sigil-lines" d="M 73 27 L 59 41" />
        </svg>
        <h1 class="logo-text">Ervelus</h1>
      </div>
    </Transition>
    <RouterView v-if="authStore.authChecked" />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore();
</script>

<style scoped>
.loader-container {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #0c0d14;
  z-index: 100;
}

.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
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

.stars::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    radial-gradient(2.5px 2.5px at 150px 150px, #fff, rgba(0,0,0,0)),
    radial-gradient(3px 3px at 200px 30px, #eee, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 10px 200px, #ddd, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 350px 350px;
  animation: animateStarLayer2 1000s linear infinite;
}

.stars::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
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

.sigil {
  stroke: rgba(255, 255, 255, 0.6);
  stroke-width: 2;
  fill: none;
  filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.9));
  animation: glow 2s ease-in-out infinite;
}

.sigil-circle {
  stroke-dasharray: 300;
  stroke-dashoffset: 300;
  animation: draw 2s ease-out forwards;
}

.sigil-lines {
  stroke-dasharray: 300;
  stroke-dashoffset: 300;
  animation: draw 5s ease-in-out forwards;
  animation-delay: 0.3s;
}

.logo-text {
  font-family: 'MedievalSharp', cursive;
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 0.2em;
  margin-top: 1.5rem;
  text-shadow: 0 0 30px rgba(255, 255, 255, 1);
  opacity: 0;
  animation: fadeInText 2s ease-in-out 1s forwards;
}

@keyframes draw {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes glow {
  0%, 100% {
    filter: drop-shadow(0 0 40px rgba(255, 255, 255, 1));
    stroke-width: 2;
  }
  50% {
    filter: drop-shadow(0 0 60px rgba(255, 255, 255, 1));
    stroke-width: 2.2;
  }
}

@keyframes fadeInText {
  to {
    opacity: 1;
  }
}

.fade-leave-active {
  transition: opacity 1.2s ease-in-out;
}

.fade-leave-from {
  opacity: 1;
}

.fade-leave-to {
  opacity: 0;
}
</style>