<template>
  <footer class="border-t border-white/10 bg-black/30 text-gray-400">
    <div class="max-w-screen-2xl mx-auto px-4 py-4 flex flex-col items-center md:flex-row md:justify-between gap-2">
      <p class="text-sm select-none">&copy; {{ year }} Ervelus. All rights reserved.</p>
      <div class="flex items-center gap-4">
        <router-link to="/privacy-policy" class="hover:text-white transition">Privacy Policy</router-link>
        <router-link to="/terms-of-service" class="hover:text-white transition">Terms of Service</router-link>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear();
</script>