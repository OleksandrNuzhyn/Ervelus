<template>
  <div class="landing-page">
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
      <div class="content-container">
        <section class="hero-section text-center">
          <h1 class="hero-title">
            We are <span class="text-gradient">Ervelus</span>
          </h1>
        </section>

        <section class="bento-grid">
          <article class="bento-item item-why">
            <div class="item-header">
              <div class="icon-wrapper">
                <EyeIcon class="item-icon" />
              </div>
              <h2 class="item-title">Our Purpose</h2>
            </div>
            <p class="item-text">
              The world around us is beautiful, but sometimes we crave more. We built Ervelus because we wanted to see the ordinary through the prism of the extraordinary. We believe everyday life can be an epic adventure.
            </p>
          </article>

          <article class="bento-item item-idea">
            <div class="item-header">
              <div class="icon-wrapper">
                <SparklesIcon class="item-icon" />
              </div>
              <h2 class="item-title">The Idea</h2>
            </div>
            <p class="item-text">
              Generative AI meets legendary aesthetics. From gritty cyberpunk to dark fantasy, we provide the tools to transform your photos into digital realms.
            </p>
          </article>

          <article class="bento-item item-stat">
            <div class="stat-number">2024</div>
            <div class="stat-label">Founded</div>
          </article>
          
          <article class="bento-item item-team">
            <div class="item-header">
              <h2 class="item-title">The Team</h2>
            </div>
            <div class="team-grid">
              <div class="team-member">
                <div class="member-avatar">ON</div>
                <div class="member-content">
                  <div class="member-header">
                    <h3 class="member-name">Oleksandr Nuzhyn</h3>
                    <div class="member-role">Founder</div>
                  </div>
                  <p class="member-bio-text">
                    Architected the backend system, developed the API, and manages the cloud infrastructure.
                  </p>
                </div>
              </div>
              
              <div class="team-member">
                <div class="member-avatar">ND</div>
                <div class="member-content">
                  <div class="member-header">
                    <h3 class="member-name">Nikita Dakhno</h3>
                    <div class="member-role">Co-Founder</div>
                  </div>
                  <p class="member-bio-text">
                    Designed the user interface, developed the frontend application, and creates AI prompts.
                  </p>
                </div>
              </div>
            </div>
          </article>
        </section>
      </div>
      <FooterComponent />
    </div>
  </div>
</template>

<script setup>
import HeaderComponent from '@/components/HeaderComponent.vue'
import FooterComponent from '@/components/FooterComponent.vue'
import {
  EyeIcon,
  SparklesIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'
</script>

<style scoped>
html, body {
  overscroll-behavior-y: none;
}

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
  
  position: relative;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--color-text-primary);
  overflow-x: hidden;
}

/* Background Elements */
.noise-overlay {
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
  opacity: 0.3;
}

.ambient-light {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 0%, rgba(139, 180, 255, 0.08), transparent 70%);
  pointer-events: none;
  z-index: 0;
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
}

.orb-1 {
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  top: -200px;
  left: -200px;
  opacity: 1;
  filter: blur(80px);
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
  opacity: 0.8;
  filter: brightness(1.7);
}

.content-container {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 135px 24px 200px;
}

.hero-section {
  text-align: center;
  margin-bottom: 52px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.hero-title {
  font-size: clamp(48px, 5vw, 72px);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #fff;
  margin-bottom: 24px;
}

.text-gradient {
  background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 30px rgba(165, 180, 252, 0.2));
  padding-right: 0.1em;
  display: inline-block;
}

.hero-subtitle {
  font-size: clamp(20px, 2vw, 24px);
  font-weight: 400;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.75);
  margin: 0 auto;
  max-width: 600px;
}

.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.bento-item {
  background: rgba(18, 18, 20, 0.75);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  padding: 32px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
}

.bento-item:hover {
  background: rgba(30, 30, 35, 0.8);
  transform: scale(1.02);
}

.item-why { grid-column: span 2; }
.item-idea { grid-column: span 1; }
.item-stat { 
  grid-column: span 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.item-team { grid-column: span 2; }
.item-team .item-header { justify-content: center; }

.item-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.icon-wrapper {
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.02);
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-icon {
  width: 24px;
  height: 24px;
  color: #fff;
}

.item-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  color: #fff;
  letter-spacing: -0.01em;
}

.item-text {
  font-size: 16px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.75);
  margin: 0;
}

.stat-number {
  font-size: 56px;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
  line-height: 1;
  letter-spacing: -0.02em;
  display: inline-block;
}

.stat-label {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 8px;
  font-weight: 500;
}

.team-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.team-member {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.member-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.member-header {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.member-avatar {
  min-width: 48px;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  border: 1px solid rgba(255, 255, 255, 0.02);
}

.member-name {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.member-role {
  font-size: 13px;
  color: #a5b4fc;
  font-weight: 500;
}

.member-bio-text {
  font-size: 14px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

@media (max-width: 900px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }
  
  .item-why, .item-idea, .item-stat, .item-team {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .team-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .content-container {
    padding: 110px 16px 80px;
  }

  .hero-section {
    margin-bottom: 40px;
  }

  .hero-title {
    font-size: clamp(36px, 10vw, 48px);
  }
}
</style>