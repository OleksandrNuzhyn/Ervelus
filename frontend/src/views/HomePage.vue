<template>
  <div>
    <HeaderComponent />
    <div class="noise-overlay"></div>
    <div class="ambient-light"></div>

    <div class="global-background">
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
      <div class="glow-orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>

    <div class="landing-wrapper">
      <section class="hero-apple">
        <div class="hero-container" @mousemove="handleGlobalMouseMove">
          <div class="hero-content">
            <div class="badge-pill">
              <span class="badge-dot"></span>
              <span>Inspired by well-known genres </span>
            </div>
            <h1 class="hero-title">
              Unleash Your <br />
              <span class="text-gradient">Digital Fantasy</span>
            </h1>
            <p class="hero-subtitle">
              Turn reality into a digital legend. Powerful algorithms unlock gate to unknown worlds with just one touch
            </p>
            <button @click="navigateToDashboard" class="cta-primary large hero-cta">
              Get Started
            </button>
          </div>

          <div class="hero-visual">
            <div class="floating-cards">
              <div class="card card-main tilt-card" ref="heroCard" @click="bringCardToFront('main')">
                <div class="card-inner">
                  <img src="@/assets/home_page/dark-fantasy_flying.webp" alt="AI Art Main" class="card-img" />
                  <div class="card-shine"></div>
                </div>
              </div>
              <div class="card card-floating card-1" @click="bringCardToFront('card1')">
                <img src="@/assets/home_page/light-fantasy_flying.webp" alt="Cyberpunk" class="card-img" />
              </div>
              <div class="card card-floating card-2" @click="bringCardToFront('card2')">
                <img src="@/assets/home_page/wild-west_flying.webp" alt="Fantasy" class="card-img" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section-comparison">
        <div class="section-header">
          <h2 class="section-title">See the transformation</h2>
          <p class="section-subtitle">
            Experience the power of AI. Drag to compare original and styled versions
          </p>
        </div>

        <div class="style-pills">
          <button v-for="style in previewStyles" :key="style.id" @click="selectedPreviewStyle = style.id"
            :class="['style-pill', { active: selectedPreviewStyle === style.id }]">
            {{ style.name }}
          </button>
        </div>

        <div class="comparison-container">
          <div class="comparison-frame">
            <div class="comparison-side before-side">
              <img :src="originalImg" class="comparison-img" alt="Original Photo" />
              <span class="comparison-label overlay-label">Original</span>
            </div>

            <div class="comparison-side after-side" :style="{ 'clip-path': `inset(0 ${100 - sliderPosition}% 0 0)` }">
              <img :src="getStyledImageUrl()" class="comparison-img" alt="Styled Result" />
              <span class="comparison-label overlay-label">{{ getCurrentStyleName() }}</span>
            </div>

            <div class="slider-handle-wrapper" :style="{ left: `${sliderPosition}%` }" @mousedown.prevent="startDrag"
              @touchstart.prevent="startDrag">
              <div class="slider-handle">
                <svg class="slider-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 9l4-4 4 4m0 6l-4 4-4-4">
                  </path>
                </svg>
              </div>
              <div class="slider-line"></div>
            </div>
          </div>

          <p class="comparison-hint">
            <svg class="hint-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"></path>
            </svg>
            Drag to compare
          </p>
        </div>
      </section>

      <section class="section-styles">
        <div class="section-header">
          <h2 class="section-title">Choose your destiny</h2>
          <p class="section-subtitle">
            Access powerful styles tailored to your needs
          </p>
        </div>

        <div class="pricing-list">
          <div v-for="tier in subscriptionTiers" :key="tier.id"
            :class="['pricing-card-horizontal', { featured: tier.featured }]">
            <div class="pricing-left">
              <div class="pricing-header-horizontal">
                <h3 class="pricing-name-horizontal">{{ tier.name }}</h3>
                <div class="pricing-price-horizontal">
                  <span class="price-currency-horizontal">$</span>
                  <span class="price-amount-horizontal">{{ tier.price }}</span>
                  <span class="price-period-horizontal">/month</span>
                </div>
              </div>
            </div>

            <div class="pricing-right">
              <div v-if="tier.includePrevious" class="previous-styles-note">
                + All styles from the "{{ tier.previousPlanName }}" plan
              </div>

              <div class="styles-grid">
                <div v-for="(style, index) in tier.styles" :key="style.id" class="style-item"
                  :style="{ 'animation-delay': `${index * 0.1}s` }">
                  <div class="style-name">{{ style.name }}</div>
                  <div class="style-genre">{{ style.genre }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section-genres">
        <div class="section-header">
          <h2 class="section-title">Legendary genres</h2>
          <p class="section-subtitle">
            From dark medieval fantasies to futuristic cyberpunk dreams
          </p>
        </div>

        <div class="genres-grid">
          <div v-for="genre in genres" :key="genre.id" class="genre-card">
            <div class="genre-icon-wrapper">
              <component :is="genre.icon" class="genre-icon" />
            </div>
            <h3 class="genre-title">{{ genre.title }}</h3>
            <p class="genre-description">{{ genre.description }}</p>
          </div>
        </div>
      </section>

      <section class="section-steps">
        <div class="section-header">
          <h2 class="section-title">Everything you need for magic</h2>
          <p class="section-subtitle">
            Just in three simple steps
          </p>
        </div>

        <div class="steps-container">
          <div v-for="(step, index) in steps" :key="step.id" class="step-item">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-icon-wrapper">
              <component :is="step.icon" class="step-icon" />
            </div>
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-description">{{ step.description }}</p>
          </div>
        </div>

      </section>

      <section class="section-product-demo">
        <div class="section-header">
          <h2 class="section-title">Product Demo</h2>
          <p class="section-subtitle">
            How it works
          </p>
        </div>

        <div class="video-container">
          <video ref="demoVideo" :src="ervelusDemoVideo" :poster="posterImg" muted loop playsinline preload="none" class="steps-video"></video>
        </div>
      </section>

      <section class="section-final-cta">
        <div class="final-cta-content">
          <h2 class="final-cta-title">Ready to enter the Ervelus?</h2>
          <p class="final-cta-subtitle">
            Give ordinary images spectacular looks based on legendary genres now
          </p>
          <button @click="navigateToDashboard" class="cta-primary large">
            Get Started
          </button>
        </div>
      </section>
    </div>
    <FooterComponent />
  </div>
</template>

<script setup>
import { ref, onUnmounted, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import originalImg from '@/assets/home_page/original.webp'
import darkFantasyResult from '@/assets/home_page/dark-fantasy_result.webp'
import lightFantasyResult from '@/assets/home_page/light-fantasy_result.webp'
import ancientGreeceResult from '@/assets/home_page/ancient-greece_result.webp'
import gildedResult from '@/assets/home_page/gilded-result.webp'
import medievalResult from '@/assets/home_page/medieval-result.webp'
import ervelusDemoVideo from '@/assets/home_page/Ervelus Demo.mp4'
import posterImg from '@/assets/home_page/poster.webp'
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue'
import FooterComponent from '@/components/HeadFootComponents/FooterComponent.vue'
import {
  FireIcon,
  SparklesIcon as SparklesHeroIcon,
  CogIcon,
  CubeIcon,
  CloudArrowUpIcon,
  SwatchIcon,
  ArrowDownTrayIcon,
  ClockIcon,
  GlobeAltIcon,
  SparklesIcon,
  ArrowTrendingUpIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const sliderPosition = ref(50)
let isDragging = false
const selectedPreviewStyle = ref('dark-fantasy')
const heroCard = ref(null)

const previewStyles = [
  { id: 'dark-fantasy', name: 'Dark Fantasy', icon: FireIcon },
  { id: 'light-fantasy', name: 'Light Fantasy', icon: SparklesHeroIcon },
  { id: 'ancient-greece', name: 'Ancient Greece', icon: GlobeAltIcon },
  { id: 'gilded', name: 'The Gilded Age', icon: SparklesIcon },
  { id: 'medieval', name: 'Medieval', icon: CubeIcon }
]

const styleImages = {
  'dark-fantasy': darkFantasyResult,
  'light-fantasy': lightFantasyResult,
  'ancient-greece': ancientGreeceResult,
  'gilded': gildedResult,
  'medieval': medievalResult
}

function getStyledImageUrl() {
  return styleImages[selectedPreviewStyle.value] || styleImages['dark-fantasy']
}

const subscriptionTiers = [
  {
    id: 'amateur',
    name: 'Amateur',
    price: 6,
    featured: false,
    includePrevious: false,
    previousPlanName: null,
    styles: [
      { id: 1, name: 'Gothic Fantasy', genre: 'Fantasy' },
      { id: 2, name: 'Light Fantasy', genre: 'Fantasy' },
      { id: 3, name: 'Steampunk', genre: 'Punkverse' },
      { id: 4, name: 'Solarpunk', genre: 'Punkverse' },
      { id: 5, name: 'Dieselpunk', genre: 'Punkverse' },
      { id: 6, name: 'Stone Age', genre: 'Time Travel' },
      { id: 7, name: 'Ancient Greece', genre: 'Time Travel' },
      { id: 8, name: 'Wonders of Giza', genre: 'Around The World' },
      { id: 9, name: 'Japanese Spring', genre: 'Around The World' },
      { id: 10, name: 'Parisian Dream', genre: 'Around The World' },
      { id: 11, name: 'Merry Christmas', genre: 'Events' },
      { id: 12, name: 'Rio de Janeiro Carnival', genre: 'Events' }
    ]
  },
  {
    id: 'journeyman',
    name: 'Journeyman',
    price: 10,
    featured: true,
    includePrevious: true,
    previousPlanName: 'Amateur',
    styles: [
      { id: 13, name: 'Dark Fantasy', genre: 'Fantasy' },
      { id: 14, name: 'Adventure Fantasy', genre: 'Fantasy' },
      { id: 15, name: 'Cyberpunk', genre: 'Punkverse' },
      { id: 16, name: 'Atompunk', genre: 'Punkverse' },
      { id: 17, name: 'The Gilded Age', genre: 'Time Travel' },
      { id: 18, name: 'Wild West', genre: 'Time Travel' },
      { id: 19, name: 'Medieval Realism', genre: 'Time Travel' },
      { id: 20, name: 'Pripyat Gloom', genre: 'Around The World' },
      { id: 21, name: 'Valentine\'s Day', genre: 'Events' },
      { id: 22, name: 'Halloween', genre: 'Events' },
      { id: 23, name: 'Hong Kong Urban', genre: 'Trending' },
      { id: 24, name: 'Tokyo Drive', genre: 'Trending' },
      { id: 25, name: 'Diplomatic Elevator', genre: 'Trending' }
    ]
  },
  {
    id: 'master',
    name: 'Master',
    price: 15,
    featured: false,
    includePrevious: true,
    previousPlanName: 'Journeyman',
    styles: [
      { id: 26, name: 'Grimdark Fantasy', genre: 'Fantasy' },
      { id: 27, name: 'Venice Canals', genre: 'Around The World' },
      { id: 28, name: 'Chinise New Year', genre: 'Events' },
      { id: 29, name: 'Dark Cinematic', genre: 'Trending' },
      { id: 30, name: 'Yacht Chillin\'', genre: 'Trending' }
    ]
  }
]

const genres = [
  {
    id: 'fantasy',
    title: 'Fantasy',
    description: 'Epic adventures in magical worlds',
    icon: FireIcon
  },
  {
    id: 'punkverse',
    title: 'Punkverse',
    description: 'Alternative worlds of technology and rebellion',
    icon: CogIcon
  },
  {
    id: 'time-travel',
    title: 'Time Travel',
    description: 'Journey through time',
    icon: ClockIcon
  },
  {
    id: 'around-the-world',
    title: 'Around the World',
    description: 'Explore distant lands',
    icon: GlobeAltIcon
  },
  {
    id: 'events',
    title: 'Events',
    description: 'Celebrations and festivals',
    icon: SparklesIcon
  },
  {
    id: 'trending',
    title: 'Trending',
    description: 'Popular styles of the moment',
    icon: ArrowTrendingUpIcon
  }
]

const steps = [
  {
    id: 'upload',
    title: 'Upload Your Image',
    description: 'Choose any photo from your gallery',
    icon: CloudArrowUpIcon
  },
  {
    id: 'style',
    title: 'Choose Your Style',
    description: 'Select from our legendary genres',
    icon: SwatchIcon
  },
  {
    id: 'generate',
    title: 'Generate & Download',
    description: 'Watch how we transform reality ',
    icon: ArrowDownTrayIcon
  }
]

function getCurrentStyleIcon() {
  const style = previewStyles.find(s => s.id === selectedPreviewStyle.value)
  return style ? style.icon : FireIcon
}

function getCurrentStyleName() {
  const style = previewStyles.find(s => s.id === selectedPreviewStyle.value)
  return style ? style.name : 'Dark Fantasy'
}

function getStyleClass(styleId) {
  return `style-${styleId}`
}

function startDrag(e) {
  isDragging = true
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchmove', handleDrag)
  document.addEventListener('touchend', stopDrag)
}

function handleDrag(e) {
  if (!isDragging) return

  const sliderElement = document.querySelector('.comparison-frame')
  if (!sliderElement) return

  const rect = sliderElement.getBoundingClientRect()
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const x = clientX - rect.left
  const percentage = (x / rect.width) * 100

  sliderPosition.value = Math.max(0, Math.min(100, percentage))
}

function stopDrag() {
  isDragging = false
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', handleDrag)
  document.removeEventListener('touchend', stopDrag)
}

function navigateToDashboard() {
  router.push('/dashboard')
}

function handleGlobalMouseMove(e) {
  if (heroCard.value) {
    const rect = heroCard.value.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    const centerX = rect.width / 2
    const centerY = rect.height / 2

    const rotateX = ((y - centerY) / centerY) * -5
    const rotateY = ((x - centerX) / centerX) * 5

    heroCard.value.style.transform = `translate(-50%, -50%) rotate(-5deg) perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`

    const shine = heroCard.value.querySelector('.card-shine')
    if (shine) {
      shine.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.2), transparent 80%)`
    }
  }
}

function bringCardToFront(cardId) {
  const cards = document.querySelectorAll('.floating-cards .card')
  cards.forEach(card => {
    card.style.zIndex = '1'
  })

  if (cardId === 'main' && heroCard.value) {
    heroCard.value.style.zIndex = '10'
  }
  else if (cardId === 'card1') {
    const card1 = document.querySelector('.card-1')
    if (card1) card1.style.zIndex = '10'
  }
  else if (cardId === 'card2') {
    const card2 = document.querySelector('.card-2')
    if (card2) card2.style.zIndex = '10'
  }
}

const demoVideo = ref(null)
let videoObserver = null

onMounted(() => {
  videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && demoVideo.value) {
        demoVideo.value.play().catch(() => {
        })
      } else if (demoVideo.value) {
        demoVideo.value.pause()
      }
    })
  }, { threshold: 0.5 })

  if (demoVideo.value) {
    videoObserver.observe(demoVideo.value)
  }
})

onUnmounted(() => {
  if (videoObserver) {
    videoObserver.disconnect()
  }
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', handleDrag)
  document.removeEventListener('touchend', stopDrag)
})
</script>

<style scoped>
.landing-wrapper {
  --color-bg: #000000;
  --color-surface: #1c1c1e;
  --color-text-primary: #ffffff;
  --color-text-secondary: #a1a1a6;
  --color-accent: #8b5cf6;
  --color-accent-hover: #a78bfa;
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 48px;
  --spacing-xl: 80px;
  --spacing-2xl: 120px;
  --radius-sm: 12px;
  --radius-md: 18px;
  --radius-lg: 24px;
  background: transparent;
  position: relative;
  z-index: 1;
  color: var(--color-text-primary);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
  min-height: 100vh;
  overflow-x: hidden;
}

.landing-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  background: transparent;
  pointer-events: none;
}

.noise-overlay {
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
  opacity: 0.4;
}

.ambient-light {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 0%, rgba(59, 130, 246, 0.05), transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.global-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;

  background-color: #000000;
  background-image: linear-gradient(to bottom, #000000, #0a0a0c);
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
  mix-blend-mode: screen;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: #3b82f6;
  top: -100px;
  left: -100px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: #60a5fa;
  bottom: -100px;
  right: -100px;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.3);
  top: 40%;
  left: 40%;
  opacity: 0.2;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(circle at center, black 40%, transparent 90%);
}

.section-title {
  font-size: clamp(40px, 5vw, 64px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--color-text-primary);
  margin: 0;
}

.section-subtitle {
  font-size: clamp(18px, 2vw, 24px);
  font-weight: 400;
  line-height: 1.5;
  color: var(--color-text-secondary);
  margin: var(--spacing-sm) 0 0;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.section-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.hero-apple {
  position: relative;
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl) var(--spacing-md);
  overflow: hidden;
}

.video-container {
  max-width: 1000px;
  margin: var(--spacing-xl) auto 0;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.steps-video {
  width: 100%;
  display: block;
}

.hero-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: left;
  max-width: 600px;
}

.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 100px;
  font-size: 14px;
  color: var(--color-accent);
  margin-bottom: 24px;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.1);
}

.badge-dot {
  width: 6px;
  height: 6px;
  background: var(--color-accent);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--color-accent);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7);
  }

  70% {
    box-shadow: 0 0 0 10px rgba(139, 92, 246, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0);
  }
}

.hero-title {
  font-size: clamp(48px, 6vw, 80px);
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.03em;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm);
}

.text-gradient {
  background: linear-gradient(135deg, #fff 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 30px rgba(139, 92, 246, 0.3));
  padding-right: 0.1em;
  display: inline-block;
}

.hero-subtitle {
  font-size: clamp(18px, 2vw, 20px);
  font-weight: 400;
  line-height: 1.6;
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-md);
  max-width: 600px;
}

.hero-description {
  font-size: clamp(18px, 2vw, 21px);
  line-height: 1.5;
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-lg);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 14px 28px;
  font-size: 17px;
  font-weight: 500;
  color: #fff;
  background: var(--color-accent);
  border: none;
  border-radius: 980px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 30px rgba(139, 92, 246, 0.5), 0 4px 16px rgba(139, 92, 246, 0.3);
}

.cta-primary:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 0 50px rgba(139, 92, 246, 0.6), 0 8px 24px rgba(139, 92, 246, 0.5);
}

.cta-primary.large {
  padding: 18px 36px;
  font-size: 19px;
}

.hero-cta {
  margin-top: var(--spacing-lg);
}

.cta-arrow {
  width: 16px;
  height: 16px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cta-primary:hover .cta-arrow {
  transform: translateX(4px);
}

.hero-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 600px;
  z-index: 1;
}

.floating-cards {
  position: relative;
  width: 100%;
  height: 600px;
  perspective: 1000px;
}

.card {
  position: absolute;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  pointer-events: auto;
  transition: filter 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  filter: brightness(1.1);
  box-shadow: 0 30px 60px -12px rgba(139, 92, 246, 0.4);
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-main {
  width: 380px;
  height: 500px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%) rotate(-5deg);
  z-index: 2;
  transition: transform 0.1s ease-out;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent 50%);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 24px;
}

.processing-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(139, 92, 246, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 100px;
  color: white;
  font-size: 13px;
  font-weight: 500;
}

.spinner {
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.card-shine {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 3;
}

.card-floating {
  width: 240px;
  height: 320px;
  z-index: 1;
  filter: brightness(0.7);
  transition: all 0.5s ease;
}

.card-floating:hover {
  filter: brightness(1);
  z-index: 3;
}

.card-1 {
  top: 10%;
  right: 0;
  transform: rotate(10deg);
  animation: float-right 8s ease-in-out infinite 1s;
}

.card-2 {
  bottom: 10%;
  left: 0;
  transform: rotate(-10deg);
  animation: float-left 7s ease-in-out infinite 2s;
}

@keyframes float-right {

  0%,
  100% {
    transform: translateY(0px) rotate(10deg);
  }

  50% {
    transform: translateY(-20px) rotate(10deg);
  }
}

@keyframes float-left {

  0%,
  100% {
    transform: translateY(0px) rotate(-10deg);
  }

  50% {
    transform: translateY(-20px) rotate(-10deg);
  }
}

section {
  position: relative;
  padding: var(--spacing-2xl) var(--spacing-md);
}

.style-pills {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-lg);
}

.style-pill {
  padding: 10px 20px;
  font-size: 15px;
  font-weight: 500;
  color: var(--color-text-secondary);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 980px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.style-pill:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.style-pill.active {
  color: #fff;
  background: var(--color-accent);
  border-color: var(--color-accent);
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
}

.comparison-container {
  max-width: 1100px;
  margin: 0 auto;
}

.comparison-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--color-surface);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.comparison-side {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  z-index: 1;
}

.before-side {
  background: linear-gradient(135deg, #1c1c1e 0%, #2c2c2e 100%);
}

.after-side {
  transition: clip-path 0.1s linear;
}

.placeholder-icon,
.styled-icon {
  width: 80px;
  height: 80px;
  opacity: 0.5;
  color: #fff;
}

.comparison-label {
  font-size: 15px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.comparison-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
}

.overlay-label {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  padding: 6px 12px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.slider-handle-wrapper {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 48px;
  transform: translateX(-50%);
  cursor: ew-resize;
  z-index: 10;
}

.slider-line {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #fff;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
  transform: translateX(-50%);
}

.slider-handle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 48px;
  height: 48px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.slider-handle-wrapper:hover .slider-handle {
  transform: translate(-50%, -50%) scale(1.1);
}

.slider-icon {
  width: 24px;
  height: 24px;
  color: #000;
}

.comparison-hint {
  margin-top: var(--spacing-md);
  text-align: center;
  font-size: 14px;
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
}

.hint-icon {
  width: 16px;
  height: 16px;
}

.pricing-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  max-width: 1400px;
  margin: 0 auto;
}

.pricing-card-horizontal {
  position: relative;
  background: rgba(28, 28, 30, 0.6);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  display: flex;
  gap: var(--spacing-lg);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.pricing-card-horizontal:hover {
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
}

.pricing-card-horizontal.featured {
  border-color: var(--color-accent);
  box-shadow: 0 0 60px rgba(139, 92, 246, 0.3), 0 20px 40px rgba(139, 92, 246, 0.2);
}

.pricing-card-horizontal.featured::before {
  content: 'Elder\'s Choice';
  position: absolute;
  top: -12px;
  left: var(--spacing-lg);
  padding: 6px 16px;
  background: var(--color-accent);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: 980px;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
}

.pricing-left {
  flex-shrink: 0;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.pricing-header-horizontal {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.pricing-name-horizontal {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  letter-spacing: -0.02em;
}

.pricing-price-horizontal {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-currency-horizontal {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.price-amount-horizontal {
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
  color: var(--color-text-primary);
}

.price-period-horizontal {
  font-size: 16px;
  color: var(--color-text-secondary);
}

.pricing-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.previous-styles-note {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: var(--radius-sm);
  color: var(--color-text-primary);
  font-size: 14px;
  font-weight: 500;
  text-align: center;
}

.styles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--spacing-sm);
  animation: fadeInGrid 0.6s ease-out;
}

@keyframes fadeInGrid {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.style-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-sm);
  padding: var(--spacing-sm);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  animation: pulse-border 3s ease-in-out infinite;
}

.style-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
      transparent,
      rgba(139, 92, 246, 0.3),
      transparent);
  animation: shimmer-continuous 3s ease-in-out infinite;
}

@keyframes shimmer-continuous {
  0% {
    left: -100%;
  }

  50% {
    left: 100%;
  }

  100% {
    left: 100%;
  }
}

@keyframes pulse-border {

  0%,
  100% {
    border-color: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 0 rgba(139, 92, 246, 0);
  }

  50% {
    border-color: rgba(139, 92, 246, 0.3);
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.2);
  }
}

.style-item:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--color-accent);
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 0 30px rgba(139, 92, 246, 0.4), 0 8px 24px rgba(139, 92, 246, 0.2);
}

.style-item:active {
  transform: translateY(-2px) scale(1);
}

.style-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 4px;
  position: relative;
  z-index: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.style-item:hover .style-name {
  color: var(--color-accent);
  transform: translateX(4px);
}

.style-genre {
  font-size: 12px;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  position: relative;
  z-index: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.style-item:hover .style-genre {
  color: rgba(255, 255, 255, 0.8);
  transform: translateX(4px);
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: var(--spacing-sm);
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-sm);
}

.genre-card {
  background: rgba(28, 28, 30, 0.5);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  text-align: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 0;
}

.genre-card:hover {
  transform: translateY(-8px);
  border-color: rgba(255, 255, 255, 0.2);
}

.genre-icon-wrapper {
  margin-bottom: var(--spacing-md);
}

.genre-icon {
  width: 40px;
  height: 40px;
  color: var(--color-accent);
  margin: 0 auto;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  filter: drop-shadow(0 0 8px rgba(139, 92, 246, 0.3));
}

.genre-card:hover .genre-icon {
  transform: scale(1.1) rotate(5deg);
  filter: drop-shadow(0 0 12px rgba(139, 92, 246, 0.5));
}

.genre-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs);
  word-wrap: break-word;
}

.genre-description {
  font-size: 13px;
  line-height: 1.4;
  color: var(--color-text-secondary);
  margin: 0;
  word-wrap: break-word;
}

.steps-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;
}

.step-item {
  text-align: center;
  padding: var(--spacing-lg);
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  margin-bottom: var(--spacing-md);
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  background: var(--color-accent);
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
}

.step-icon-wrapper {
  margin-bottom: var(--spacing-md);
}

.step-icon {
  width: 56px;
  height: 56px;
  color: var(--color-text-secondary);
  margin: 0 auto;
}

.step-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm);
}

.step-description {
  font-size: 16px;
  line-height: 1.5;
  color: var(--color-text-secondary);
  margin: 0;
}

.section-final-cta {
  padding: var(--spacing-2xl) var(--spacing-md);
}

.final-cta-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.final-cta-title {
  font-size: clamp(36px, 5vw, 56px);
  font-weight: 700;
  line-height: 1.1;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-md);
}

.final-cta-subtitle {
  font-size: clamp(18px, 2vw, 21px);
  line-height: 1.5;
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-lg);
}

.section-final-cta .cta-primary {
  margin-bottom: 150px;
}

footer {
  position: relative;
  z-index: 2;
}

@media (min-width: 640px) and (max-width: 1024px) {
  .hero-subtitle {
    margin-left: auto;
    margin-right: auto;
    text-align: center;
  }
}

@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
    text-align: center;
  }

  .hero-content {
    max-width: 100%;
    text-align: center;
  }

  .hero-subtitle {
    margin-left: auto;
    margin-right: auto;
  }

  .hero-visual {
    min-height: 400px;
  }

  .floating-cards {
    height: 400px;
  }

  .card-main {
    width: 280px;
    height: 380px;
  }

  .card-floating {
    width: 180px;
    height: 240px;
  }
}

@media (max-width: 768px) {
  section {
    padding: var(--spacing-xl) var(--spacing-sm);
  }

  .hero-apple {
    min-height: auto;
    padding-top: 120px;
    padding-bottom: 60px;
    align-items: flex-start;
  }

  .card-floating {
    display: none;
  }

  .hero-container {
    gap: var(--spacing-lg);
  }

  .hero-content {
    margin-bottom: 0;
  }

  .hero-visual {
    min-height: auto;
    margin-top: 40px;
  }

  .floating-cards {
    height: 390px;
  }

  .card-main {
    width: 280px;
    height: 390px;
    transform: translate(-50%, -50%) !important;
    animation: none !important;
    transition: none !important;
    box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.5);
  }

  .pricing-card-horizontal {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .pricing-card-horizontal.featured::before {
    left: 50%;
    transform: translateX(-50%);
  }

  .pricing-left {
    min-width: auto;
    text-align: center;
  }

  .pricing-header-horizontal {
    align-items: center;
  }

  .pricing-price-horizontal {
    justify-content: center;
  }

  .styles-grid {
    grid-template-columns: 1fr;
  }

  .genres-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-xs);
  }

  .genre-card {
    padding: var(--spacing-sm);
  }

  .genre-title {
    font-size: 16px;
  }

  .genre-description {
    font-size: 12px;
  }

  .genre-icon {
    width: 32px;
    height: 32px;
  }

  .steps-container {
    grid-template-columns: 1fr;
  }

  .style-pills {
    gap: 6px;
  }

  .style-pill {
    padding: 8px 16px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .hero-apple {
    min-height: 70vh;
  }

  .hero-content {
    padding: 0 var(--spacing-xs);
  }

  .badge-pill {
    font-size: 12px;
    padding: 4px 10px;
  }

  .comparison-frame {
    aspect-ratio: 4 / 3;
  }

  .genres-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-xs);
    padding: 0 var(--spacing-xs);
  }

  .genre-card {
    padding: var(--spacing-sm);
  }

  .genre-title {
    font-size: 14px;
  }

  .genre-description {
    font-size: 11px;
  }

  .genre-icon {
    width: 28px;
    height: 28px;
  }
}
</style>