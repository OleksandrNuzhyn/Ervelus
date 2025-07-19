<template>
  <div class="w-full max-w-6xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
    <div class="text-center mb-7">
      <h1 class="text-4xl font-bold text-white md:text-5xl">
        Pricing Plans
      </h1>
      <p class="mt-4 text-xl text-gray-400 md:text-2xl">
        Choose the plan that's right for you.
      </p>
    </div>

    <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
      <div 
        v-for="plan in plans" 
        :key="plan.name" 
        class="flex flex-col rounded-lg shadow-lg bg-white/5 backdrop-blur-md border border-white/1"
      >
        <div class="px-6 py-8">
          <h2 class="text-2xl font text-center text-white">{{ plan.name }}</h2>
          <p class="mt-2 text-md text-center text-gray-400">{{ plan.description }}</p>
          <div class="mt-6 text-center">
            <span class="text-5xl font-bold text-white">{{ plan.price }}</span>
            <span class="text-base font-medium text-gray-400">/month</span>
          </div>
        </div>
        
        <div class="flex-1 flex flex-col justify-between px-6 pt-6 pb-8">
          <ul class="space-y-4">
            <li v-for="feature in plan.features" :key="feature" class="flex items-start">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-green-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p class="ml-3 text-base text-gray-300">{{ feature }}</p>
            </li>
          </ul>
          <div class="mt-8">
            <button class="w-full py-3 font-bold text-white text-xl transition duration-300 rounded-md bg-white/10 backdrop-blur-md border border-white/5 shadow-md hover:bg-white/20">
              Buy
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
    name: 'Basic',
    description: 'For individuals starting out.',
    price: '$6',
    features: [
      '10 projects',
      '5 GB of storage',
      'just buy pls'
    ]
  },
  {
    name: 'Premium',
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
    name: 'Enterprise',
    description: 'For large organizations.',
    price: '$99',
    features: [
      'Unlimited projects & storage',
      'Custom analytics',
      '24/7 dedicated support',
      'SSO integration',
      'Custom branding',
      'Custom domains'
    ]
  }
]);
</script>
