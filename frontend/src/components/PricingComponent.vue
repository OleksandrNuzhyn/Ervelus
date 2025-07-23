<template>
  <div class="w-full max-w-screen-2xl mx-auto px-8 pt-14 pb-16">
    <div class="text-center mb-9">
      <h1 class="text-4xl font-bold text-gray-500 md:text-5xl medieval">
        Contracts
      </h1>
    </div>

    <div class="grid grid-cols-1 gap-7 md:grid-cols-3 transform relative translate-x-6 translate-y-8 md:translate-y-34">
      <div 
        v-for="plan in plans" 
        :key="plan.name" 
        class="plan-card relative flex flex-col transform w-[410px] h-[620px]"
      >
        <div class="px-6 py-3">
          <h2 class="text-3xl font text-center text-black medieval">{{ plan.name }}</h2>
          <p class="mt-2 text-md text-center text-black">{{ plan.description }}</p>
          <div class="mt-6 text-center">
            <span class="text-5xl font-bold text-black">{{ plan.price }}</span>
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
            <button @click="buy(plan)" class="inline-flex justify-center p-0 transform hover:scale-103 transition focus:outline-none select-none">
              <img src="@/assets/button.webp" alt="Buy plan"/>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const plans = ref([
  {
    name: 'Amateur',
    description: 'For individuals starting out.',
    price: '$6',
    features: [
      '10 projects',
      '5 GB of storage',
      'just buy pls',
    ]
  },
  {
    name: 'Journeyman',
    description: 'For small teams and professionals.',
    price: '$29',
    features: [
      'Unlimited projects',
      '50 GB of storage',
      'Advanced analytics',
      'Priority email support'
    ]
  },
  {
    name: 'Master',
    description: 'For large organizations.',
    price: '$99',
    features: [
      'Unlimited projects & storage',
      'Custom analytics',
      '24/7 dedicated support',
      'SSO integration',
      'and more'
    ]
  }
]);

function buy(plan){
  console.log('Purchase',plan.name);
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

</style>
