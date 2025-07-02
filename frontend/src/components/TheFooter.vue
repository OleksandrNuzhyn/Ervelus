<template>
    <footer class="bg-white">
      <div class="w-full max-w-7xl px-4 py-12 mx-auto overflow-hidden sm:px-6 lg:px-8">
        <nav class="flex flex-wrap justify-center -mx-5 -my-2" aria-label="Footer">
          <div class="px-5 py-2">
            <RouterLink to="/terms-of-service" class="text-base text-gray-500 hover:text-gray-900">Правила використання</RouterLink>
          </div>
          <div class="px-5 py-2">
            <RouterLink to="/privacy-policy" class="text-base text-gray-500 hover:text-gray-900">Політика конфіденційності</RouterLink>
          </div>
        </nav>
        <p class="mt-8 text-base text-center text-gray-400">
          © {{ new Date().getFullYear() }} SaaS Project. Всі права захищено.
        </p>
      </div>
    </footer>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router';
  </script>