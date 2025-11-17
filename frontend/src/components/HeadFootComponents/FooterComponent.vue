<template>
  <footer class="border-t border-white/10 bg-black/30 text-gray-400">
    <div class="max-w-screen mx-auto px-4 sm:px-6 lg:px-12 py-4 flex flex-col items-center md:flex-row md:justify-between gap-2">
      <div class="flex flex-row items-center gap-2">
        <img src="/favicon.svg" alt="Ervelus Logo" class="h-8 w-8" />
        <p class="text-sm select-none">&copy; {{ year }} Ervelus. All rights reserved. Made with 🧙‍♂️</p>
      </div>
      <div class="flex items-center gap-4">
        <router-link to="/terms-of-service" class="hover:text-white transition">Terms of Service</router-link>
        <router-link to="/privacy-policy" class="hover:text-white transition">Privacy Policy</router-link>
        <router-link to="/cookie-policy" class="hover:text-white transition">Cookie Policy</router-link>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear();
</script>