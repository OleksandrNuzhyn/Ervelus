<template>
  <footer class="border-t border-white/10 bg-black/30 text-gray-400 py-12 md:pb-16 md:pt-12">
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-12">
        <div class="col-span-1 md:col-span-5">
          <div class="flex items-center gap-2 mb-4">
            <img src="/favicon.svg" alt="Ervelus Logo" class="h-8 w-8" />
            <span class="text-xl font-bold text-white tracking-tight">Ervelus</span>
          </div>
          <p class="select-none">&copy; {{ year }} Ervelus. All rights reserved</p>
        </div>

        <div class="col-span-1 md:col-span-3 md:col-start-7">
          <h3 class="text-white font-semibold text-lg mb-4">Company</h3>
          <ul class="space-y-3">
            <li><router-link to="/about-us" class="hover:text-white transition-colors duration-200">About Us</router-link></li>
            <li><a href="mailto:support@ervelus.com" class="text-[#93c5fd] hover:text-[#60a5fa] transition-colors duration-200">support@ervelus.com</a></li>
          </ul>
        </div>

        <div class="col-span-1 md:col-span-3">
          <h3 class="text-white font-semibold text-lg mb-4">Legal</h3>
          <ul class="space-y-3">
            <li><router-link to="/terms-of-service" class="hover:text-white transition-colors duration-200">Terms of Service</router-link></li>
            <li><router-link to="/privacy-policy" class="hover:text-white transition-colors duration-200">Privacy Policy</router-link></li>
            <li><router-link to="/refund-policy" class="hover:text-white transition-colors duration-200">Refund Policy</router-link></li>
            <li><router-link to="/cookie-policy" class="hover:text-white transition-colors duration-200">Cookie Policy</router-link></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear();
</script>