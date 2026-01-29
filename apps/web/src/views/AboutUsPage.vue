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
            <span class="text-gradient-white">We are</span> <span class="text-accent">Ervelus</span>
          </h1>
        </section>

        <section class="bento-grid">
          <article class="bento-item item-why">
            <div class="item-header">
              <EyeIcon class="item-icon" />
              <h2 class="item-title">Our Purpose</h2>
            </div>
            <p class="item-text">
              The world around us is beautiful, but sometimes we crave more. We built Ervelus because we wanted to see the ordinary through the prism of the extraordinary. We believe everyday life can be an epic adventure.
            </p>
          </article>

          <article class="bento-item item-idea">
            <div class="item-header">
              <SparklesIcon class="item-icon" />
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
                  <div class="member-bio">
                    <p>Software Engineering student at NTUU "KPI" (Kyiv).</p>
                    <p><span class="bio-label">Role:</span> Architected the secure, scalable backend and managed the infrastructure.</p>
                    <p><span class="bio-label">Focus:</span> System Architecture, API Engineering, System Deployment.</p>
                  </div>
                </div>
              </div>
              
              <div class="team-member">
                <div class="member-avatar">ND</div>
                <div class="member-content">
                  <div class="member-header">
                    <h3 class="member-name">Nikita Dakhno</h3>
                    <div class="member-role">Co-Founder & Frontend Engineer</div>
                  </div>
                  <div class="member-bio">
                    <p>Computer Science student at TUKE (Slovakia).</p>
                    <p><span class="bio-label">Role:</span> Designed the UI/UX and developed the client-side application.</p>
                    <p><span class="bio-label">Focus:</span> UI/UX Design, Frontend Engineering, AI Prompt Logic.</p>
                  </div>
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
  padding: 120px 24px 120px;
}

.hero-section {
  margin-bottom: 40px;
  max-width: 900px;
}

.hero-title {
  font-size: clamp(48px, 10vw, 120px);
  font-weight: 800;
  line-height: 0.95;
  letter-spacing: -0.04em;
  margin: 0 0 32px;
  white-space: nowrap;
}

.text-gradient-white {
  background: linear-gradient(135deg, #fff 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 30px rgba(139, 92, 246, 0.3));
  padding-right: 0.05em;
  display: inline;
}

.text-accent {
  color: #fff;
  text-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
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
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  
  padding: 40px;
  border-radius: 24px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.bento-item:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(139, 92, 246, 0.5);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(139, 92, 246, 0.2);
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
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.01em;
  color: #fff;
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
  gap: 20px;
  align-items: flex-start;
}

.member-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.member-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-avatar {
  min-width: 52px;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.05));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 19px;
  border: 1px solid rgba(139, 92, 246, 0.3);
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.member-name {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.member-role {
  font-size: 14px;
  color: #a78bfa;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.member-bio {
  font-size: 15px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.member-bio p {
  margin: 0;
}

.bio-label {
  color: #fff;
  font-weight: 700;
  font-size: 14px;
  margin-right: 4px;
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
    font-size: clamp(32px, 12vw, 56px);
  }
}
</style>