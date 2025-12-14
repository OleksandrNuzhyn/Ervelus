<template>
  <div>
    <HeaderComponent />
    <div class="page-wrapper">
      <div class="global-background">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="grid-overlay"></div>
      </div>

      <div class="content-container">
        <section class="hero-section">
          <h1 class="hero-title">
            We are <span class="text-accent">Ervelus</span>
          </h1>
          <p class="hero-subtitle">
            Unleash your fantasy
          </p>
        </section>

        <section class="bento-grid">
          <article class="bento-item item-why">
            <div class="item-header">
              <EyeIcon class="item-icon" />
              <h2 class="item-title">Our Purpose</h2>
            </div>
            <p class="item-text">
              The world around us is beautiful, but sometimes we crave more.
              We built Ervelus because we wanted to see the ordinary through the prism of the extraordinary.
              We believe everyday life can be an epic adventure.
            </p>
          </article>

          <article class="bento-item item-idea">
            <div class="item-header">
              <SparklesIcon class="item-icon" />
              <h2 class="item-title">The Idea</h2>
            </div>
            <p class="item-text">
              Generative AI meets legendary aesthetics. From gritty cyberpunk to dark fantasy,
              we provide the tools to transform your photos into digital realms.
            </p>
          </article>

          <article class="bento-item item-stat">
            <div class="stat-number">2024</div>
            <div class="stat-label">Founded</div>
          </article>
          <article class="bento-item item-team">
            <div class="item-header">
              <UserGroupIcon class="item-icon" />
              <h2 class="item-title">The Team</h2>
            </div>
            <div class="team-grid">

              <div class="team-member">
                <div class="member-avatar">ON</div>
                <div class="member-content">
                  <div class="member-header">
                    <h3 class="member-name">Oleksandr Nuzhyn</h3>
                    <div class="member-role">Founder & Lead Architect</div>
                  </div>
                  <p class="member-bio">
                    Software Engineering student at NTUU "KPI" (Kyiv).
                    <span class="bio-highlight">Role:</span> Architected the secure, scalable RESTful backend using
                    Python
                    (Django).
                    Managed the entire infrastructure deployment on Google Cloud Platform (Cloud Run, Cloud SQL) and
                    implemented AI models.
                    <br><span class="bio-highlight">Focus:</span> Cloud Architecture, Backend Logic, System Deployment.
                  </p>
                </div>
              </div>

              <div class="team-member">
                <div class="member-avatar">ND</div>
                <div class="member-content">
                  <div class="member-header">
                    <h3 class="member-name">Nikita Dakhno</h3>
                    <div class="member-role">Co-Founder & Frontend Engineer</div>
                  </div>
                  <p class="member-bio">
                    Computer Science student at TUKE (Slovakia).
                    <span class="bio-highlight">Role:</span> Designed and developed the responsive client-side
                    application
                    using Vue.js.
                    Responsible for the complete UI/UX design and collaborates on prompt engineering logic to ensure
                    high-quality artistic outputs.
                    <br><span class="bio-highlight">Focus:</span> Frontend Development, User Experience, Prompt Logic.
                  </p>
                </div>
              </div>

            </div>
          </article>
        </section>
      </div>
    </div>
    <FooterComponent />
  </div>
</template>

<script setup>
import HeaderComponent from '@/components/HeadFootComponents/HeaderComponent.vue'
import FooterComponent from '@/components/HeadFootComponents/FooterComponent.vue'
import {
  EyeIcon,
  SparklesIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'
</script>

<style scoped>
.page-wrapper {
  --color-bg: #050505;
  --color-surface: #121212;
  --color-border: #27272a;
  --color-text-primary: #ffffff;
  --color-text-secondary: #a1a1a6;
  --color-accent: #8b5cf6;

  position: relative;
  min-height: 100vh;
  background-color: var(--color-bg);
  color: var(--color-text-primary);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  overflow-x: hidden;
}

.global-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(150px);
  opacity: 0.15;
}

.orb-1 {
  width: 800px;
  height: 800px;
  background: var(--color-accent);
  top: -200px;
  left: -200px;
}

.orb-2 {
  width: 600px;
  height: 600px;
  background: #3b82f6;
  bottom: -100px;
  right: -100px;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(circle at center, black 60%, transparent 100%);
  opacity: 0.5;
}

.content-container {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 160px 24px 120px;
}

.hero-section {
  margin-bottom: 100px;
  max-width: 900px;
}

.hero-title {
  font-size: clamp(64px, 10vw, 120px);
  font-weight: 800;
  line-height: 0.95;
  letter-spacing: -0.04em;
  margin: 0 0 32px;
}

.text-accent {
  color: var(--color-accent);
}

.hero-subtitle {
  font-size: clamp(20px, 4vw, 28px);
  color: var(--color-text-secondary);
  font-weight: 400;
  max-width: 600px;
  line-height: 1.4;
}

.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto auto;
  gap: 24px;
}

.bento-item {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  padding: 40px;
  border-radius: 24px;
  transition: border-color 0.3s ease, transform 0.3s ease;
}

.bento-item:hover {
  border-color: var(--color-accent);
  transform: translateY(-4px);
}

.item-why {
  grid-column: span 2;
}

.item-idea {
  grid-column: span 1;
}

.item-stat {
  grid-column: span 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: linear-gradient(135deg, var(--color-surface) 0%, #1a1a20 100%);
}

.item-team {
  grid-column: span 2;
}

.item-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.item-icon {
  width: 28px;
  height: 28px;
  color: var(--color-accent);
}

.item-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  letter-spacing: -0.02em;
}

.item-text {
  font-size: 18px;
  line-height: 1.6;
  color: var(--color-text-secondary);
  margin: 0;
}

.stat-number {
  font-size: 64px;
  font-weight: 800;
  color: #fff;
  line-height: 1;
  letter-spacing: -0.03em;
}

.stat-label {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-secondary);
  margin-top: 8px;
}

.team-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
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
  gap: 4px;
}

.member-avatar {
  min-width: 48px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.1);
  color: var(--color-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  border: 1px solid rgba(139, 92, 246, 0.2);
  flex-shrink: 0;
}

.member-name {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.member-role {
  font-size: 14px;
  color: var(--color-accent);
  font-weight: 500;
}

.member-bio {
  font-size: 15px;
  line-height: 1.6;
  color: var(--color-text-secondary);
  margin: 0;
}

.bio-highlight {
  color: #fff;
  font-weight: 600;
}

@media (max-width: 768px) {
  .team-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}

@media (max-width: 900px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }

  .item-why,
  .item-idea,
  .item-stat,
  .item-team {
    grid-column: span 1;
  }

  .hero-title {
    font-size: 56px;
  }
}
</style>