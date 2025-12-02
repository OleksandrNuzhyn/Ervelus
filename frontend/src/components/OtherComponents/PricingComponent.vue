<template>
  <div v-if="!isLoading">
    <div class="w-full max-w-screen-2xl mx-auto px-2 pb-8">
      <div :class="['grid grid-cols-1 gap-7 justify-items-center mt-4 plans-grid', grid_col_num]">
        <div 
          v-for="(plan, index) in plans"
          :key="plan.name"
          :class="['plan-card relative flex flex-col w-full md:max-w-md h-[700px] plan-card-static-highlight', { 'plan-card-selected-highlight': highlightedIndex === index }]"
          @mouseover="handleMouseOver(index)"
          @mouseleave="handleMouseLeave"
        >
          <div class="flex flex-col h-full p-8 text-center">
            <h2 class="text-5xl scribe-text font-bold mt-7 mb-4" style="text-shadow: 0px 0px 3px rgba(0, 0, 0, 1), 0 0 45px rgba(255, 255, 255, 0.8);">{{ plan.name }}</h2>

            <div class="mb-4">
              <span class="text-5xl font-bold scribe-text">
                ${{ formatPrice(plan.price) }}
              </span>
              <span class="text-2xl scribe-text">/month</span>
              <p class="mt-4 text-2xl scribe-text">{{ plan.description }}</p>
            </div>

            <div class="separator">
              <div class="separator-diamond"></div>
            </div>

            <ul class="space-y-4 flex-1">
              <li v-for="feature in plan.features" :key="feature" class="flex items-center justify-center">
                <div class="flex-shrink-0">
                  <svg class="h-4 w-4 feature-icon-shadow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M12 2L3 5v6c0 5.25 3.75 10.5 9 12 5.25-1.5 9-6.75 9-12V5l-9-3z" fill="#211F1D"/>
                  </svg>
                </div>
                <p class="ml-3 text-3xl scribe-text">{{ feature }}</p>
              </li>
            </ul>
            <div class="absolute inset-x-0 bottom-4 flex justify-center">
              <template v-if="plan.is_active">
                <button @click="buy(plan)" class="inline-flex justify-center p-0 transform transition focus:outline-none select-none button-white-shadow">
                  <img src="@/assets/pricing_assets/button.png" alt="Buy plan"/>
                </button>
              </template>
              <div v-else class="text-5xl scribe-text font-bold font-nothing-you-could-do mb-13" style="text-shadow: 0px 0px 3px rgba(0, 0, 0, 0.8), 0 0 85px rgba(255, 255, 255, 1);">
                Unavailable
              </div>
            </div>

          </div>
        </div>
      </div>

      <div class="parchment-wrapper fade-in-policy">
        <p class="main-text-font">
          Prices exclude VAT / Local taxes
        </p>
      </div>
    </div>

    <div v-if="showLoginModal" @click.self="showLoginModal = false" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-[7px]">
      <div class="w-full max-w-[340px] p-8 mx-4 text-center shadow-2xl rounded-2xl backdrop-blur-[14px] bg-[rgba(10,10,10,0.3)]">
          <h2 class="text-3xl font-bold mb-8 medieval medieval-title medieval-main-title-shadow">Authentication Required</h2>
          <router-link 
              to="/login" 
              class="w-full flex justify-start items-center text-almost-black pl-29 router-link-login"
          >
              <img src="@/assets/svg/login.svg" alt="Login" class="w-9 h-9 login-icon-default" />
          </router-link>
      </div>
    </div>

    <div v-if="showEligibilityModal" @click.self="showEligibilityModal = false; message = ''; modalTitle = ''" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-[7px]">
      <div class="w-full max-w-[340px] p-8 mx-4 text-center shadow-2xl rounded-2xl backdrop-blur-[14px] bg-[rgba(10,10,10,0.3)]">
          <h2 class="text-3xl font-bold mb-8 medieval medieval-title medieval-main-title-shadow">{{ modalTitle }}</h2>
          <p class="text-xl main-text-font">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import api from '@/services/api';

const auth = useAuthStore();
const plans = ref([]);
const showLoginModal = ref(false);
const showEligibilityModal = ref(false);
const isLoading = ref(true);
const message = ref('');
const modalTitle = ref('');
const highlightedIndex = ref(1);

const grid_col_num = computed(() => {
  if (plans.value.length >= 3) return 'xl:grid-cols-3';
  if (plans.value.length === 2) return 'xl:grid-cols-2';
  return '';
});

function formatPrice(price) {
  const num = parseFloat(price);
  if (Number.isInteger(num)) {
    return num.toString();
  }
  return num.toFixed(2);
}

function handleMouseOver(index) {
  highlightedIndex.value = index;
}

function handleMouseLeave() {
  highlightedIndex.value = 1;
}

async function getSubscriptionPlans() {
  try {
    const response = await api.get('/api/products/subscription-plans/');
    plans.value = response.data.map(plan => ({...plan}));
  }
  catch {
    plans.value = [];
  }
  finally {
    isLoading.value = false;
  }
}

async function buy(plan) {
  if (!auth.isAuthenticated) {
    showLoginModal.value = true;
    return;
  }
  if (!window.Paddle) {
    return;
  }
  if (!plan.paddle_price_id) {
    return;
  }

  message.value = '';
  modalTitle.value = '';

  try {
    await api.get('/api/subscriptions/subscription-eligibility/', { params: { plan_id: plan.id } });
    window.Paddle.Checkout.open({
      items: [
        { priceId: plan.paddle_price_id, quantity: 1 }
      ],
      customer: {
        email: auth.user.email
      },
      customData: {
        user_id: auth.user.pk
      }
    });
  }
  catch (error) {
    if (error.response) {
      if (error.response.status === 404) {
        message.value = 'The selected plan is unavailable';
        modalTitle.value = 'Plan Inactive';
      }
      else if (error.response.status === 400) {
        message.value = 'Purchase unavailable due to budget limits. We apologize for the inconvenience — improvements are underway';
        modalTitle.value = 'Purchase Unavailable';
      }
      else {
        message.value = 'An unexpected error occurred. Please try again later';
        modalTitle.value = 'Error';
      }
      showEligibilityModal.value = true;
    }
    else {
      message.value = 'Network error or no response from server';
      modalTitle.value = 'Error';
      showEligibilityModal.value = true;
    }
  }
}

onMounted(() => {
  getSubscriptionPlans();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nothing+You+Could+Do&display=swap');
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;770&family=EB+Garamond&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Uncial+Antiqua&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Macondo+Swash+Caps&display=swap');
.medieval{font-family:'MedievalSharp',cursive;}
.heading-font{font-family: 'Cinzel Decorative', 'Uncial Antiqua', cursive;}
.font-nothing-you-could-do{font-family: 'Nothing You Could Do', cursive;}
.main-text-font { font-family: 'Lora', 'EB Garamond', serif; }
.text-almost-black{color:#1c1c1c;}
.text-dark-blood{color:#4a2323;}
.medieval-title {
  color: transparent;
  background-image: linear-gradient(
    75deg,
    #1A2024 0%,
    #3B4246 2%,
    #6F7D82 4%,
    #4A5458 6%,
    #AAB2B6 8%,
    #6F7D82 10%,
    #AAB2B6 12%,
    #8B9599 15%,
    #E2E8EC 20%,
    #FFFFFF 25%,
    #D4DBDF 28%,
    #7A8488 30%,
    #B8C2C6 35%,
    #E2E8EC 40%,
    #FFFFFF 45%,
    #AAB2B6 50%,
    #6F7D82 55%,
    #E2E8EC 60%,
    #9CA3A6 65%,
    #7A8488 70%,
    #AAB2B6 75%,
    #5B6366 80%,
    #3B4246 85%,
    #1A2024 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  opacity: 0.85;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.5), 
               0 0 12px rgba(0, 10, 15, 0.8);
  filter: blur(0.7px);
}

.medieval-main-title-shadow {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.45), 
               0 0 15px rgba(0, 10, 15, 0.8);
}

.scribe-text {
  font-family: 'Macondo Swash Caps', cursive;
  color: #1A1A1A;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

.parchment-wrapper {
  position: relative;
  z-index: 9;
  max-width: 550px;
  margin: 1.4rem auto 0;
  padding: 1.3rem 1rem;
  background-image: url('@/assets/pricing_assets/paper.webp');
  background-size: 100% 100%;
  background-position: center;
  text-align: center;
  filter: brightness(0.85);
  display: flex;
  justify-content: center;
  align-items: center;
}

.parchment-wrapper p {
  font-size: 1rem;
  color: #000;
  text-shadow: 0 0 30px rgba(255, 255, 255, 0.7);
  font-weight: 600;
}

.parchment-link {
  color: #000;
  text-decoration: underline;
}

.login-icon-default {
  filter: invert(0.8) sepia(0.2) saturate(0.5) drop-shadow(0px 0px 5px rgba(0, 0, 0, 0.8)) drop-shadow(0px 0px 20px rgba(255, 255, 255, 0.6));
  transition: filter 0.5s ease-in-out;
}

.feature-icon-shadow {
  filter: drop-shadow(0px 0px 1px rgba(0, 0, 0, 0.5));
}

.plan-card {
  position: relative;
  isolation: isolate;
  transition: all 0.6s ease-in-out;
  filter: drop-shadow(0 15px 30px rgba(10, 25, 30, 0.5));
}

.plan-card-static-highlight {
  filter: drop-shadow(0 0 20px rgba(15, 35, 40, 0.8)) drop-shadow(0 0 45px rgba(20, 100, 120, 0.25));
}

.plan-card.recommended {
  filter: drop-shadow(0 0 15px rgba(20, 100, 120, 0.4));
}

.plan-card-selected-highlight {
  filter: drop-shadow(0 0px 50px rgba(15, 35, 40, 0.7)) drop-shadow(0 0 40px rgba(20, 100, 120, 0.6));
}

.button-white-shadow {
  filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.08));
  transition: filter 0.4s ease-in-out;
}

.button-white-shadow:hover {
  filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.08)) brightness(0.8);
}

.plan-card::before{
  content:'';
  position:absolute;
  inset:0;
  background-image:url('@/assets/pricing_assets/paper.webp');
  background-size:100% 100%;
  background-position:center;
  background-repeat:no-repeat;
  z-index:-1;
  filter: brightness(1.12);
}

.separator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1rem 0;
}

.separator::before,
.separator::after {
  content: '';
  flex-grow: 1;
  height: 1px;
  background-color: transparent;
  background-image: linear-gradient(
    75deg,
    #362F27 0%,
    #38312b 20%,
    #302e3b 40%,
    #473D35 60%,
    #362F27 80%,
    #2B251F 100%
  );
  opacity: 0.7;
  filter: blur(0.7px);
  margin-left: 2rem;
  margin-right: 2rem;
}

.separator-diamond {
  width: 8px;
  height: 8px;
  background-color: transparent;
  background-image: linear-gradient(
    75deg,
    #362F27 0%,
    #473D35 20%,
    #5C5247 40%,
    #473D35 60%,
    #362F27 80%,
    #2B251F 100%
  );
  opacity: 0.7;
  transform: rotate(45deg);
  margin: 0 1rem;
  box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.8), 0 0 5px rgba(0, 0, 0, 0.7);
  filter: blur(0.7px);
}

@media (max-width: 767px) {
  .plan-card {
    width: 28rem !important;
    max-width: 100%;
  }
}

.plan-card {
  opacity: 0;
  animation: fadeIn 0.9s ease-in-out forwards;
}

.plan-card:nth-child(1) {
  animation-delay: 0.12s;
}

.plan-card:nth-child(2) {
  animation-delay: 0.18s;
}

.plan-card:nth-child(3) {
  animation-delay: 0.21s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(25px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in-policy {
  opacity: 0;
  animation: fadeIn 0.9s ease-in-out forwards;
  animation-delay: 0.18s;
}

.router-link-login:hover img {
  filter: invert(0.5) sepia(0.2) saturate(0.5);
}

.plans-grid {
  position: relative;
  z-index: 10;
}
</style>