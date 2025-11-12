<template>
  <div>
    <HeaderComponent />
    <div class="landing-wrapper">
      <section class="hero-apple">
        <div class="hero-content">
          <h1 class="hero-title">
            Unleash Your Fantasy
          </h1>
          <p class="hero-subtitle">
            Countless Worlds In Your Pocket
          </p>
          <p class="hero-description">
            Give ordinary images spectacular looks based on legendary genres
          </p>
        </div>
        
        <div class="hero-visual">
          <div class="preview-card preview-card-1">
            <div class="card-shimmer"></div>
          </div>
          <div class="preview-card preview-card-2">
            <div class="card-shimmer"></div>
          </div>
          <div class="preview-card preview-card-3">
            <div class="card-shimmer"></div>
          </div>
        </div>
      </section>
  
      <section class="section-comparison">
        <div class="section-header">
          <h2 class="section-title">See the transformation</h2>
          <p class="section-subtitle">
            Experience the power of AI. Drag to compare original and styled versions.
          </p>
        </div>

        <div class="style-pills">
          <button
            v-for="style in previewStyles"
            :key="style.id"
            @click="selectedPreviewStyle = style.id"
            :class="['style-pill', { active: selectedPreviewStyle === style.id }]"
          >
            {{ style.name }}
          </button>
        </div>

        <div class="comparison-container">
          <div class="comparison-frame">
            <div class="comparison-side before-side">
              <div class="comparison-placeholder">
                <svg class="placeholder-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                <span class="comparison-label">Original</span>
              </div>
            </div>

            <div 
              class="comparison-side after-side"
              :style="{ 'clip-path': `inset(0 ${100 - sliderPosition}% 0 0)` }"
            >
              <div class="comparison-styled" :class="getStyleClass(selectedPreviewStyle)">
                <component :is="getCurrentStyleIcon()" class="styled-icon" />
                <span class="comparison-label">{{ getCurrentStyleName() }}</span>
              </div>
            </div>

            <div
              class="slider-handle-wrapper"
              :style="{ left: `${sliderPosition}%` }"
              @mousedown.prevent="startDrag"
              @touchstart.prevent="startDrag"
            >
              <div class="slider-handle">
                <svg class="slider-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 9l4-4 4 4m0 6l-4 4-4-4"></path>
                </svg>
              </div>
              <div class="slider-line"></div>
            </div>
          </div>

          <p class="comparison-hint">
            <svg class="hint-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"></path>
            </svg>
            Drag to compare
          </p>
        </div>
      </section>

      <section class="section-styles">
        <div class="section-header">
          <h2 class="section-title">Choose your plan</h2>
          <p class="section-subtitle">
            Access powerful AI styles tailored to your creative needs
          </p>
        </div>

        <div class="pricing-list">
          <div 
            v-for="tier in subscriptionTiers"
            :key="tier.id"
            :class="['pricing-card-horizontal', { featured: tier.featured }]"
          >
            <div class="pricing-left">
              <div class="pricing-header-horizontal">
                <h3 class="pricing-name-horizontal">{{ tier.name }}</h3>
                <div class="pricing-price-horizontal">
                  <span class="price-currency-horizontal">$</span>
                  <span class="price-amount-horizontal">{{ tier.price }}</span>
                  <span class="price-period-horizontal">/місяць</span>
                </div>
              </div>
            </div>

            <div class="pricing-right">
              <div v-if="tier.includePrevious" class="previous-styles-note">
                + Всі стилі з плану "{{ tier.previousPlanName }}"
              </div>
              
              <div class="styles-grid">
                <div 
                  v-for="(style, index) in tier.styles"
                  :key="style.id"
                  class="style-item"
                  :style="{ 'animation-delay': `${index * 0.1}s` }"
                >
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
          <div 
            v-for="genre in genres"
            :key="genre.id"
            class="genre-card"
          >
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
          <div 
            v-for="(step, index) in steps"
            :key="step.id"
            class="step-item"
          >
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-icon-wrapper">
              <component :is="step.icon" class="step-icon" />
            </div>
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-description">{{ step.description }}</p>
          </div>
        </div>
      </section>

      <section class="section-final-cta">
        <div class="final-cta-content">
          <h2 class="final-cta-title">Ready to create?</h2>
          <p class="final-cta-subtitle">
            Start transforming your images today
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
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue'
import FooterComponent from '@/components/HeadFootComponents/FooterComponent.vue'
import { 
  FireIcon,
  BeakerIcon,
  SparklesIcon as SparklesHeroIcon,
  CogIcon,
  CubeIcon,
  CloudArrowUpIcon,
  SwatchIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const sliderPosition = ref(50)
let isDragging = false
const selectedPreviewStyle = ref('dark-fantasy')

const previewStyles = [
  { id: 'dark-fantasy', name: 'Dark Fantasy', icon: FireIcon },
  { id: 'gothic-horror', name: 'Gothic Horror', icon: BeakerIcon },
  { id: 'cyberpunk', name: 'Cyberpunk', icon: CubeIcon },
  { id: 'steampunk', name: 'Steampunk', icon: CogIcon },
  { id: 'anime', name: 'Anime', icon: SparklesHeroIcon }
]

const subscriptionTiers = [
  {
    id: 'free',
    name: 'Безкоштовний',
    price: 0,
    featured: false,
    includePrevious: false,
    previousPlanName: null,
    styles: [
      { id: 1, name: 'Класичний портрет', genre: 'Класика' },
      { id: 2, name: 'Вінтаж', genre: 'Ретро' },
      { id: 3, name: 'Чорно-білий', genre: 'Монохром' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 4, name: 'Акварель', genre: 'Мистецтво' },
      { id: 5, name: 'Ескіз', genre: 'Графіка' }
    ]
  },
  {
    id: 'pro',
    name: 'Professional',
    price: 29,
    featured: true,
    includePrevious: true,
    previousPlanName: 'Безкоштовний',
    styles: [
      { id: 6, name: 'Темне фентезі', genre: 'Dark Fantasy' },
      { id: 7, name: 'Готичний жах', genre: 'Gothic Horror' },
      { id: 8, name: 'Кіберпанк', genre: 'Sci-Fi' },
      { id: 9, name: 'Стімпанк', genre: 'Steampunk Noir' },
      { id: 10, name: 'Аніме', genre: 'Anime' },
      { id: 11, name: 'Олійний живопис', genre: 'Мистецтво' },
      { id: 12, name: 'Поп-арт', genre: 'Сучасне' },
      { id: 13, name: 'Імпресіонізм', genre: 'Класика' },
      { id: 14, name: 'Коміксний', genre: 'Графіка' },
      { id: 15, name: 'Піксель-арт', genre: 'Ретро' }
    ]
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 99,
    featured: false,
    includePrevious: true,
    previousPlanName: 'Professional',
    styles: [
      { id: 16, name: 'Гіперреалізм', genre: 'Реалізм' },
      { id: 17, name: 'Квантове мистецтво', genre: 'Sci-Fi' },
      { id: 18, name: 'Божественне світло', genre: 'Mythic' },
      { id: 19, name: 'Неонова ніч', genre: 'Cyberpunk' },
      { id: 20, name: 'Космічна одіссея', genre: 'Sci-Fi' },
      { id: 21, name: 'Драконячий гнів', genre: 'Dark Fantasy' },
      { id: 22, name: 'Магічні руни', genre: 'Arcane' },
      { id: 23, name: 'Кастомний AI', genre: 'Custom' }
    ]
  }
]

const genres = [
  {
    id: 'dark-fantasy',
    title: 'Epic Dark Fantasy',
    description: 'Dragons, magic, and ancient powers',
    icon: FireIcon
  },
  {
    id: 'gothic-horror',
    title: 'Gothic Horror',
    description: 'Shadows, mysteries, and dark tales',
    icon: BeakerIcon
  },
  {
    id: 'mythic-scifi',
    title: 'Mythic Sci-Fi',
    description: 'Cosmic wonders and stellar myths',
    icon: SparklesHeroIcon
  },
  {
    id: 'steampunk-noir',
    title: 'Steampunk Noir',
    description: 'Gears, steam, and dark mechanics',
    icon: CogIcon
  },
  {
    id: 'arcane-cyber',
    title: 'Arcane Cyberpunk',
    description: 'Digital magic and neon runes',
    icon: CubeIcon
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

// Functions
const getCurrentStyleIcon = () => {
  const style = previewStyles.find(s => s.id === selectedPreviewStyle.value)
  return style ? style.icon : FireIcon
}

const getCurrentStyleName = () => {
  const style = previewStyles.find(s => s.id === selectedPreviewStyle.value)
  return style ? style.name : 'Dark Fantasy'
}

const getStyleClass = (styleId) => {
  return `style-${styleId}`
}

const startDrag = (e) => {
  isDragging = true
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchmove', handleDrag)
  document.addEventListener('touchend', stopDrag)
}

const handleDrag = (e) => {
  if (!isDragging) return

  const sliderElement = document.querySelector('.comparison-frame')
  if (!sliderElement) return

  const rect = sliderElement.getBoundingClientRect()
  // Handle both mouse and touch events
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const x = clientX - rect.left
  const percentage = (x / rect.width) * 100

  sliderPosition.value = Math.max(0, Math.min(100, percentage))
}

const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', handleDrag)
  document.removeEventListener('touchend', stopDrag)
}

const navigateToDashboard = () => {
  router.push('/dashboard')
}

onUnmounted(() => {
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
  --color-accent: #0071e3;
  --color-accent-hover: #0077ed;
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 48px;
  --spacing-xl: 80px;
  --spacing-2xl: 120px;
  --radius-sm: 12px;
  --radius-md: 18px;
  --radius-lg: 24px;

  background-image: url('@/assets/background_assets/side_background.webp');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  position: relative;
  color: var(--color-text-primary);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}

.landing-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.8) 100%);
  pointer-events: none;
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

/* Hero Section - Apple Style */
.hero-apple {
  position: relative;
  min-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl) var(--spacing-md);
  overflow: hidden;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 980px;
  margin: 0 auto;
}

.hero-title {
  font-size: clamp(48px, 6vw, 80px);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.03em;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm);
  background: linear-gradient(180deg, #ffffff 0%, #a1a1a6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent; /* Fallback */
}

.hero-subtitle {
  font-size: clamp(32px, 4vw, 56px);
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-md);
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
  box-shadow: 0 4px 16px rgba(0, 113, 227, 0.3);
}

.cta-primary:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 113, 227, 0.4);
}

.cta-primary.large {
  padding: 18px 36px;
  font-size: 19px;
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
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.preview-card {
  position: absolute;
  width: 280px;
  height: 380px;
  background: rgba(28, 28, 30, 0.5);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.preview-card-1 {
  top: 15%;
  left: 5%;
  animation: float 6s ease-in-out infinite;
}

.preview-card-2 {
  top: 50%;
  right: 8%;
  animation: float 8s ease-in-out infinite 1s;
}

.preview-card-3 {
  bottom: 10%;
  left: 10%;
  animation: float 7s ease-in-out infinite 2s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.card-shimmer {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.05),
    transparent
  );
  animation: shimmer-anim 3s infinite;
}

@keyframes shimmer-anim {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
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
}

.before-side {
  background: linear-gradient(135deg, #1c1c1e 0%, #2c2c2e 100%);
}

.after-side {
  transition: clip-path 0.1s linear;
}

.comparison-placeholder,
.comparison-styled {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
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

.comparison-styled {
  color: #fff;
}
.style-dark-fantasy { background: linear-gradient(135deg, #4c1d95 0%, #1e1b4b 100%); }
.style-gothic-horror { background: linear-gradient(135deg, #7f1d1d 0%, #000000 100%); }
.style-cyberpunk { background: linear-gradient(135deg, #06b6d4 0%, #7c3aed 100%); }
.style-steampunk { background: linear-gradient(135deg, #b45309 0%, #1c1917 100%); }
.style-anime { background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%); }

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

.section-styles {
  background: rgba(0, 0, 0, 0.1);
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
  box-shadow: 0 20px 40px rgba(0, 113, 227, 0.2);
}

.pricing-card-horizontal.featured::before {
  content: 'Популярний';
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
  background: rgba(0, 113, 227, 0.1);
  border: 1px solid rgba(0, 113, 227, 0.3);
  border-radius: var(--radius-sm);
  color: var(--color-accent);
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
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 113, 227, 0.3),
    transparent
  );
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
  0%, 100% {
    border-color: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 0 rgba(0, 113, 227, 0);
  }
  
  50% {
    border-color: rgba(0, 113, 227, 0.3);
    box-shadow: 0 0 15px rgba(0, 113, 227, 0.2);
  }
}

.style-item:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--color-accent);
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 24px rgba(0, 113, 227, 0.2);
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


.section-genres {
  background: rgba(0, 0, 0, 0.1);
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--spacing-md);
  max-width: 1200px;
  margin: 0 auto;
}

.genre-card {
  background: rgba(28, 28, 30, 0.5);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  text-align: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.genre-card:hover {
  transform: translateY(-8px);
  border-color: rgba(255, 255, 255, 0.2);
}

.genre-icon-wrapper {
  margin-bottom: var(--spacing-md);
}

.genre-icon {
  width: 48px;
  height: 48px;
  color: var(--color-accent);
  margin: 0 auto;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.genre-card:hover .genre-icon {
  transform: scale(1.1) rotate(5deg);
}

.genre-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm);
}

.genre-description {
  font-size: 14px;
  line-height: 1.5;
  color: var(--color-text-secondary);
  margin: 0;
}

.section-steps {
  background: rgba(0, 0, 0, 0.2);
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

/* Final CTA */
.section-final-cta {
  background: rgba(0, 0, 0, 0.2);
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

/* Responsive */
@media (max-width: 768px) {
  section {
    padding: var(--spacing-xl) var(--spacing-sm);
  }

  .preview-card {
    display: none;
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

  .genres-grid,
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

  .comparison-frame {
    aspect-ratio: 4 / 3;
  }
}
</style>