<template>
  <div class="w-full max-w-screen-2xl mx-auto px-1 md:px-8 pt-5 pb-16">
    <div class="text-center mb-9">
      <h1 class="text-4xl font-bold text-gray-500 md:text-5xl medieval">
        Contracts
      </h1>
    </div>

    <div class="grid grid-cols-1 gap-7 xl:grid-cols-2 justify-items-center mt-8 md:mt-12">
      <div 
        v-for="plan in plans" 
        :key="plan.name" 
        class="plan-card relative flex flex-col w-full md:max-w-md h-[700px]"
      >
        <div class="px-6 py-10">
          <h2 class="text-3xl font text-center text-gray-500 medieval">{{ plan.name }}</h2>
          <p class="mt-2 text-xl text-center text-black">{{ plan.description }}</p>
          <div class="mt-6 text-center">
            <span class="text-5xl font-bold text-black">${{ formatPrice(plan.price) }}</span>
            <span class="text-base font-medium text-black">/month</span>
          </div>
        </div>
        
        <div class="flex-1 flex flex-col px-12 pt-12 relative">
          <ul class="space-y-8 flex-1">
            <li v-for="feature in plan.features" :key="feature" class="flex items-start">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-green-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p class="ml-3 text-lg text-black medieval">{{ feature }}</p>
            </li>
          </ul>
          <div class="absolute inset-x-0 bottom-2 flex justify-center">
            <template v-if="plan.is_active">
                <button @click="buy(plan)" class="inline-flex justify-center p-0 transform hover:scale-103 transition focus:outline-none select-none">
                    <img src="@/assets/button.webp" alt="Buy plan"/>
                </button>
            </template>
            <div v-else class="text-sm text-gray-500 font-bold medieval">Currently Unavailable</div>
          </div>
        </div>
      </div>
    </div>
  </div>

<div v-if="showLoginModal" @click.self="showLoginModal = false" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm transition-opacity duration-300">
    <div class="bg-gray-900/80 border border-gray-700 rounded-lg p-8 w-full max-w-sm mx-4 text-center shadow-2xl">
        <h2 class="text-2xl font-bold text-white mb-4 medieval">Authentication Required</h2>
        <p class="text-gray-300 mb-8">Please log in to purchase a subscription plan.</p>
        <router-link 
            to="/login" 
            class="w-full inline-block px-6 py-3 rounded-lg bg-gray-700/90 text-white font-semibold hover:bg-gray-600/90 border border-gray-600 transition-all duration-200"
        >
            Login
        </router-link>
    </div>
</div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import { onMounted } from 'vue';
import api from '@/services/api';

const auth = useAuthStore();
const plans = ref([]);
const showLoginModal = ref(false);

onMounted(async () => {
    const response = await api.get('/api/products/subscription-plans/');
    plans.value = response.data.map(plan => ({
      ...plan,
      priceId: plan.paddle_price_id
    }));
});

function formatPrice(price) {
  const num = parseFloat(price);
  if (Number.isInteger(num)) {
    return num.toString();
  }
  return num.toFixed(2);
}


function buy(plan){
  if (!auth.isAuthenticated) {
    showLoginModal.value = true;
    return;
  }
  if (!window.Paddle) {
    return;
  }
  if (!plan.priceId) {
    return;
  }

  window.Paddle.Checkout.open({
    items: [
      { priceId: plan.priceId, quantity: 1 }
    ],
    theme: 'dark',
    displayMode: 'overlay'
  });
}
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
.medieval{font-family:'MedievalSharp',cursive;}

.plan-card {
  position: relative;
  isolation: isolate;
}

.plan-card::before{
  content:'';
  position:absolute;
  inset:0;
  background-image:url('@/assets/paper.webp');
  background-size:100% 100%;
  background-position:center;
  background-repeat:no-repeat;
  z-index:-1;
}

@media (max-width: 767px) {
  .plan-card {
    width: 28rem !important;
    max-width: 100%;
  }
}

</style>
