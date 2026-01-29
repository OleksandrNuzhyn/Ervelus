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
            <div class="v-spacer"></div>
            
            <div class="hero-text-decor-group">
              <!-- Badge removed to reduce clutter/pile effect -->

              <h1 class="hero-title">
                Transform Your <br />
                Photos <span class="text-gradient">into AI Art</span>
              </h1>

              <p class="hero-subtitle">
                Professional AI styling. 30+ styles available
              </p>
            </div>

            <div class="v-spacer"></div>

            <div class="hero-visual-mobile md:hidden">
              <div class="floating-cards-mobile">
                <div class="card-m card-1"><img src="@/assets/home_page/paris-flying.webp" alt="1" /></div>
                <div class="card-m card-2"><img src="@/assets/home_page/elevator-flying.webp" alt="2" /></div>
                <div class="card-m card-3"><img src="@/assets/home_page/urban-flying.webp" alt="3" /></div>
              </div>
            </div>

            <div class="v-spacer"></div>

            <a href="https://t.me/ervelus_bot" target="_blank" class="cta-primary large hero-cta">
              Launch App
            </a>
          </div>
          <div class="hero-visual hidden md:block">
            <div class="floating-cards">
              <div class="card card-main tilt-card" ref="heroCard" @click="bringCardToFront('main')">
                <div class="card-inner">
                  <img src="@/assets/home_page/paris-flying.webp" alt="AI Art Main" class="card-img" />
                  <div class="card-shine"></div>
                </div>
              </div>
              <div class="card card-floating card-1" @click="bringCardToFront('card1')">
                <img src="@/assets/home_page/urban-flying.webp" alt="Urban" class="card-img" />
              </div>
              <div class="card card-floating card-2" @click="bringCardToFront('card2')">
                <img src="@/assets/home_page/elevator-flying.webp" alt="Elevator" class="card-img" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section-comparison">
        <div class="section-header">
          <h2 class="section-title">See the Difference</h2>
          <p class="section-subtitle">
            Drag the slider to compare original photo and AI result
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
              <img :src="originalImg" class="comparison-img" alt="Original Photo" loading="lazy" />
            </div>

            <div class="comparison-side after-side" :style="{ 'clip-path': `inset(0 ${100 - sliderPosition}% 0 0)` }">
              <img :src="getStyledImageUrl()" class="comparison-img" alt="Styled Result" loading="lazy" />
            </div>

            <span class="comparison-label overlay-label">
              {{ sliderPosition > 50 ? getCurrentStyleName() : 'Original' }}
            </span>

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
          <h2 class="section-title">Style Library</h2>
          <p class="section-subtitle">
            Explore our collection of creative styles
          </p>
        </div>

        <div class="styles-listing-container">
          <div class="styles-listing-grid">
            <div v-for="category in styleCategories" :key="category.id" class="style-category-card">
              <div class="card-header">
                <div class="icon-wrapper">
                  <component :is="category.icon" class="category-icon" />
                </div>
                <div>
                  <h3 class="category-name">{{ category.name }}</h3>
                  <p class="category-desc">{{ category.description }}</p>
                </div>
              </div>
              
              <div class="style-tags-wrapper">
                <span v-for="style in category.styles" :key="style" class="style-tag-pill">
                  {{ style }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section-steps">
        <div class="section-header">
          <h2 class="section-title">How it Works</h2>
          <p class="section-subtitle">
            Transform your photos in three simple steps
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
          <h2 class="section-title">See It in Action</h2>
          <p class="section-subtitle">
            Watch the real-time generation process
          </p>
        </div>

        <div class="video-container">
          <video ref="demoVideo" :src="ervelusDemoVideo" :poster="posterImg" muted loop playsinline preload="none" class="steps-video"></video>
        </div>
      </section>
    </div>
    <FooterComponent />
  </div>
</template>

<script setup>
import { ref, onUnmounted, onMounted, computed } from 'vue'
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
  ArrowTrendingUpIcon,
  ChevronDownIcon
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

const styleCategories = [
  {
    id: 'fantasy',
    name: 'Fantasy',
    description: 'Aesthetics of mythical realms and legendary creatures',
    icon: FireIcon,
    styles: ['Gothic Fantasy', 'Light Fantasy', 'Dark Fantasy', 'Adventure Fantasy', 'Grimdark Fantasy']
  },
  {
    id: 'punkverse',
    name: 'Punkverse',
    description: 'Fusion of urban subcultures and technology',
    icon: CogIcon,
    styles: ['Steampunk', 'Solarpunk', 'Dieselpunk', 'Cyberpunk', 'Atompunk']
  },
  {
    id: 'time-travel',
    name: 'Time Travel',
    description: 'Visual immersion into different historical epochs',
    icon: ClockIcon,
     styles: ['Stone Age', 'Ancient Greece', 'The Gilded Age', 'Wild West', 'Medieval Realism']
  },
  {
    id: 'around-the-world',
    name: 'Around The World',
    description: 'Iconic locations and distinct spots across the globe',
    icon: GlobeAltIcon,
    styles: ['Wonders of Giza', 'Japanese Spring', 'Parisian Dream', 'Pripyat Gloom', 'Venice Canals']
  },
  {
    id: 'events',
    name: 'Events',
    description: 'Stylized visuals for festive and large-scale gatherings',
    icon: SparklesIcon,
    styles: ['Merry Christmas', 'Rio de Janeiro Carnival', "Valentine's Day", 'Halloween', 'Chinese New Year']
  },
  {
    id: 'trending',
    name: 'Trending',
    description: 'Cinematic photography and high-quality visual aesthetics',
    icon: ArrowTrendingUpIcon,
    styles: ['Hong Kong Urban', 'Tokyo Drive', 'Diplomatic Elevator', 'Dark Cinematic', "Yacht Chillin'"]
  }
]

/* 'genres' computed property removed as it is now merged into styleCategories */

const steps = computed(() => [
  {
    id: 'upload',
    title: 'Upload Your Photo',
    description: 'Upload a selfie, portrait, or any image from your gallery',
    icon: CloudArrowUpIcon
  },
  {
    id: 'style',
    title: 'Choose Your Style',
    description: 'Choose from 30+ professional styles',
    icon: SwatchIcon
  },
  {
    id: 'generate',
    title: 'Transform & Download',
    description: 'Download high-quality art instantly. Ready to share',
    icon: ArrowDownTrayIcon
  }
])

function getCurrentStyleName() {
  const style = previewStyles.find(s => s.id === selectedPreviewStyle.value)
  return style ? style.name : 'Dark Fantasy'
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

function handleTryFree() {
  router.push('/register')
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

<style>
html, body {
  overscroll-behavior-y: none;
}
</style>

<style scoped>
.landing-wrapper {
  --color-bg: #0c0d14;
  --color-surface: #1c1c1e;
  --color-text-primary: #ffffff;
  --color-text-secondary: #a1a1a6;
  --color-accent: #ffffff;
  --color-accent-hover: #e5e5e5;
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 48px;
  --spacing-xl: 80px;
  --spacing-2xl: 120px;
  --radius-sm: 12px;
  --radius-md: 16px;
  --radius-lg: 16px;
  --radius-card: 16px;
  background: transparent;
  position: relative;
  z-index: 1;
  color: var(--color-text-primary);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
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
  opacity: 0.3;
  display: block;
}

.ambient-light {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* Cool white/blue glow for saturation */
  background: radial-gradient(circle at 50% 0%, rgba(139, 180, 255, 0.08), transparent 70%);
  pointer-events: none;
  z-index: 0;
  display: block; 
}

.global-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background-color: #0c0d14;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.2;
  mix-blend-mode: screen;
  display: block;
}

.orb-1 {
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%); /* Soft white glow */
  top: -200px;
  left: -200px;
  opacity: 1; /* Gradient handles opacity */
  filter: blur(80px); /* Reduced blur as gradient is soft */
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: #94a3b8;
  bottom: -100px;
  right: -100px;
  opacity: 0.1;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.2);
  top: 40%;
  left: 40%;
  opacity: 0.1;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(circle at 50% 40%, black 60%, transparent 100%);
  opacity: 0.5;
  display: block;
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
  border: 1px solid rgba(255, 255, 255, 0.02);
}

.steps-video {
  width: 100%;
  display: block;
}

.hero-container {
  display: grid;
  grid-template-columns: 1.4fr 1fr; /* Give more space to text column (approx 60/40) */
  gap: 40px; /* Reducing gap slightly to help space */
  align-items: center;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  min-height: 85vh; /* Enough height but not too much */
  padding-top: 0;
}

.hero-content {
  position: relative;
  z-index: 2;
  z-index: 2;
  text-align: left;
  max-width: none; /* Let grid define width */
}

.hero-badge-minimal {
  display: inline-flex;
  align-items: center;
  margin-bottom: 24px;
  position: relative;
}

/* Removed vertical border styling for cleaner look */
.hero-text-decor-group {
  display: block;
  text-align: left;
  padding-left: 0;
  border: none;
  margin-bottom: 24px; /* Reduced bottom margin */
}

/* Enhancing Mobile Layout for the Group */
/* Removed mobile border override as border is gone */

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
  font-size: clamp(48px, 5vw, 72px); /* Much larger Apple-style */
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-md); /* Increased margin */
}

.text-gradient {
  background: linear-gradient(135deg, #fff 30%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.2));
  padding-right: 0.1em;
  display: inline-block;
}

.hero-subtitle {
  font-size: clamp(20px, 2vw, 24px); /* Larger subtitle */
  font-weight: 400;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.6);
  margin: 0 0 32px;
  max-width: 700px; /* Increased to ensure 1 line */
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

/* High Contrast Pills (White BG, Black Text) */
/* Glassy Pill Style */
.hero-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px; /* Smaller padding */
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 9999px;
  margin-bottom: 24px;
  transform-origin: left;
  transition: transform 0.3s ease, background 0.3s ease;
}

.hero-badge-pill:hover {
  transform: scale(1.02);
  background: rgba(255, 255, 255, 0.12);
}

.badge-text {
  font-size: 12px;
  font-weight: 600;
  color: #fff; /* White text for glass */
  letter-spacing: 0.08em;
  /* text-transform: uppercase; Removed */
}

.badge-dot {
  width: 5px;
  height: 5px;
  background: #fff;
  border-radius: 50%;
  animation: pulse-white 2s infinite;
}

@keyframes pulse-white {
  0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); }
  70% { box-shadow: 0 0 0 4px rgba(255, 255, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
}

.cta-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 16px 32px;
  font-size: 17px;
  font-weight: 700;
  color: #000;
  background: #ffffff;
  border: none;
  border-radius: 980px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 40px rgba(255, 255, 255, 0.15), 0 0 20px rgba(255, 255, 255, 0.1);
}

.cta-primary:hover {
  background: #e2e8f0;
  transform: translateY(-2px);
  box-shadow: 0 0 60px rgba(255, 255, 255, 0.3), 0 0 30px rgba(255, 255, 255, 0.2);
}

.cta-primary.large {
  padding: 18px 36px;
  font-size: 19px;
  min-height: 58px;
}

.hero-cta {
  margin-top: 16px; /* Reduced from large spacing */
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
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.02);
  cursor: pointer;
  pointer-events: auto;
  transition: filter 0.3s ease, box-shadow 0.3s ease;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
}

.card:hover {
  filter: brightness(1.1);
  box-shadow: 0 30px 60px -12px rgba(255, 255, 255, 0.25); /* White glow instead of violet */
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
  right: -10%; /* Move outwards */
  transform: rotate(12deg);
  animation: float-right 8s ease-in-out infinite 1s;
}

.card-2 {
  bottom: 5%;
  left: -10%; /* Move outwards */
  transform: rotate(-12deg);
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
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.02);
  border-radius: 980px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.style-pill:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.style-pill.active {
  color: #000;
  background: #ffffff;
  border-color: #ffffff;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
  font-weight: 700;
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

.styles-listing-container {
  max-width: 1200px;
  margin: 0 auto;
  /* Removed double padding, reliance on section padding */
}

.styles-listing-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
  max-width: 1000px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .styles-listing-grid {
    grid-template-columns: 1fr; /* Single column on mobile */
  }
}

.style-category-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  padding: 32px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.style-category-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.icon-wrapper {
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.category-icon {
  width: 24px;
  height: 24px;
  color: #fff;
}

.category-name {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 4px 0;
}

.category-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.4;
  margin: 0;
}

.style-tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 8px; /* Kept 8px, but wide card should fix per-row issue */
}

/* Removed old category header style */

.style-tag-pill {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.04);
  padding: 8px 16px;
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.02);
  transition: all 0.2s ease;
  line-height: 1.4;
  font-weight: 500;
}

.style-tag-pill:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff !important;
  border-color: rgba(255, 255, 255, 0.05);
  transform: translateY(-1px);
  box-shadow: none;
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
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  padding: var(--spacing-md);
  text-align: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 0;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
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
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.2));
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
  color: #000000;
  background: #ffffff;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
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
  section {
    padding: var(--spacing-xl) var(--spacing-sm); /* Unified 16px side padding for all sections on mobile */
  }

  .hero-container {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
    text-align: center;
  }

  .hero-content {
    max-width: 100%;
    text-align: center;
  }

  @media (max-width: 768px) {
    .hero-apple {
      height: 100dvh;
      min-height: 100dvh;
      display: flex;
      flex-direction: column;
      padding: 0;
      overflow: hidden;
    }

    .hero-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      width: 100%;
      height: 100%;
      box-sizing: border-box;
      padding: 0 var(--spacing-sm);
    }

    .hero-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
      padding-top: 70px;
      padding-bottom: 30px;
    }

    .v-spacer {
      flex: 1;
      width: 100%;
      min-height: 10px;
    }

    .v-spacer:nth-child(1) {
      flex: 0.9;
    }

    .v-spacer:nth-child(3) {
      flex: 0.2;
    }

    .v-spacer:nth-child(5),
    .v-spacer:nth-child(7) {
      flex: 2.5;
    }

    .hero-text-group {
      flex: 0 0 auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
      z-index: 10;
    }

    .badge-pill {
      margin: 0;
      display: inline-flex;
      z-index: 10;
      background: rgba(255, 255, 255, 0.02) !important;
      border: 1px solid rgba(255, 255, 255, 0.05) !important;
      padding: 5px 16px;
      border-radius: 20px;
      backdrop-filter: blur(4px);
      animation: shimmerBorder 10s infinite ease-in-out;
    }

    @keyframes shimmerBorder {
      0%, 100% { 
        border-color: rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 10px rgba(255, 255, 255, 0); 
      }
      50% { 
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.12);
      }
    }

    .badge-shimmer {
      font-size: 13px;
      color: rgba(255, 255, 255, 0.75);
      text-transform: none;
      letter-spacing: normal;
      font-weight: 400;
      background: none;
      -webkit-text-fill-color: initial;
      animation: none;
    }

    .hero-title {
      font-size: clamp(26px, 7.5vw, 32px);
      line-height: 1.1;
      margin-bottom: 12px;
    }

    .hero-visual {
      display: none !important;
    }

    .hero-visual-mobile {
      flex: 0 1 auto;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 35vh;
      min-height: 160px;
      max-height: 45vh;
      width: 100%;
      position: relative;
    }

    .floating-cards-mobile {
      position: relative;
      height: 100%;
      width: 100%;
    }

    .card-m {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 25vh;
      height: 34vh;
      max-width: 240px;
      max-height: 320px;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 15px 40px rgba(0,0,0,0.6);
      transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
      border: 1px solid rgba(255,255,255,0.15);
    }

    .card-m img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    @keyframes heroCycle {
      0%, 28% { z-index: 10; transform: translate(-50%, -50%) scale(1); opacity: 1; filter: blur(0); }
      33.33%, 61.33% { z-index: 5; transform: translate(-20%, -55%) scale(0.85) rotate(6deg); opacity: 0.6; filter: blur(3px); }
      66.66%, 94.66% { z-index: 1; transform: translate(-80%, -55%) scale(0.85) rotate(-6deg); opacity: 0.6; filter: blur(3px); }
      100% { z-index: 10; transform: translate(-50%, -50%) scale(1); opacity: 1; filter: blur(0); }
    }

    .card-1 { animation: heroCycle 6s infinite 0s; }
    .card-2 { animation: heroCycle 6s infinite -2s; }
    .card-3 { animation: heroCycle 6s infinite -4s; }

    .hero-subtitle {
      font-size: 13.5px;
      color: rgba(255, 255, 255, 0.82);
      margin-bottom: 0;
      display: block;
      font-weight: 300;
      text-align: center;
      max-width: 240px;
      margin-left: auto;
      margin-right: auto;
      line-height: 1.4;
      text-wrap: balance;
    }

    .hero-cta {
      width: 100%;
      max-width: 280px;
      margin: 0 !important;
      display: flex;
      justify-content: center;
    }
  }

  @media (max-width: 768px) and (max-height: 700px) {
    .hero-content {
      padding-top: 60px;
      padding-bottom: 20px;
    }

    .v-spacer:first-child {
      flex: 0.4;
      min-height: 2px;
    }

    .hero-visual-mobile {
      min-height: 140px; 
      height: 25vh;
    }

    .card-m {
      width: 150px;
      height: 200px;
    }

    .hero-title {
      font-size: 26px;
      margin-bottom: 4px;
    }
    
    .v-spacer {
      min-height: 8px; 
    }
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

  .style-toggle-btn {
    display: flex !important;
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

  .style-toggle-btn {
    display: flex;
    margin-bottom: var(--spacing-sm);
  }

  .styles-collapsible {
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .styles-collapsible.expanded {
    grid-template-rows: 1fr;
  }

  .styles-content-wrapper {
    overflow: hidden;
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
    padding-top: 100px;
  }

  .hero-content {
    padding: 0 var(--spacing-xs);
  }

  .hero-title {
    font-size: 34px;
    line-height: 1.1;
  }

  .hero-subtitle {
    font-size: 13px;
    line-height: 1.6;
    opacity: 0.75;
    font-weight: 300;
    max-width: 250px;
    margin-left: auto;
    margin-right: auto;
  }

  @media (max-width: 380px) {
    .hero-title {
      font-size: 28px;
    }
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

.badge-dot.pulse {
  background: #8b5cf6;
  box-shadow: 0 0 0 rgba(139, 92, 246, 0.4);
  animation: pulse-enhanced 2s infinite;
}

@keyframes pulse-enhanced {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(139, 92, 246, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0);
  }
}

.badge-free-trial {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.1));
  border: 1px solid rgba(139, 92, 246, 0.3);
  box-shadow: 0 0 30px rgba(139, 92, 246, 0.2), 0 4px 16px rgba(139, 92, 246, 0.1);
  animation: badge-glow 7s ease-in-out infinite;
}

@keyframes badge-glow {
  0%, 100% {
    box-shadow: 0 0 30px rgba(139, 92, 246, 0.2), 0 4px 16px rgba(139, 92, 246, 0.1);
  }
  50% {
    box-shadow: 0 0 40px rgba(139, 92, 246, 0.4), 0 4px 20px rgba(139, 92, 246, 0.2);
  }
}

.badge-shimmer {
  background: linear-gradient(
    90deg,
    #fff 0%,
    #a78bfa 50%,
    #fff 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer-text 7s linear infinite;
  font-weight: 600;
}

@keyframes shimmer-text {
  0% {
    background-position: 200% center;
  }
  100% {
    background-position: -200% center;
  }
}

.free-highlight {
  color: #a78bfa;
  font-weight: 700;
  text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
  position: relative;
  display: inline-block;
  animation: glow-pulse 2s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% {
    text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
  }
  50% {
    text-shadow: 0 0 30px rgba(139, 92, 246, 0.8), 0 0 40px rgba(139, 92, 246, 0.4);
  }
}

.free-highlight-dark {
  color: #a78bfa;
  font-weight: 700;
  background: linear-gradient(135deg, #a78bfa, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  display: inline-block;
  text-shadow: none;
}

@media (max-width: 768px) {
  .badge-shimmer {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .badge-free-trial {
    padding: 6px 12px;
    font-size: 11px;
  }
  
  .badge-shimmer {
    font-size: 11px;
  }
}


@media (max-width: 768px) {
  .styles-listing-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .style-category-group {
    padding: 16px;
  }
  
  .category-header {
    margin-bottom: 12px;
    padding-bottom: 8px;
  }
  
  .category-name {
    font-size: 16px;
  }
}
</style>