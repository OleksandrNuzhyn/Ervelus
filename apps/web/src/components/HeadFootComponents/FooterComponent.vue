<template>
  <footer class="border-t border-white/10 bg-black/30 text-gray-400 pt-12 pb-16">
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-12">
        <div class="col-span-1 md:col-span-5">
          <div class="flex items-center gap-2 mb-4">
            <img src="/favicon.svg" alt="Ervelus Logo" class="h-8 w-8" />
            <span class="text-xl font-bold text-white tracking-tight">Ervelus</span>
          </div>
          <p class="text-sm select-none">&copy; {{ year }} Ervelus. All rights reserved.</p>
        </div>

        <div class="col-span-1 md:col-span-3 md:col-start-7">
          <h3 class="text-white font-semibold text-lg mb-4">Company</h3>
          <ul class="space-y-3">
            <li><router-link to="/about-us" class="hover:text-white transition-colors duration-200">About Us</router-link></li>
            <li>
              <a href="https://discord.gg/38NV8t57th" target="_blank" rel="noopener noreferrer"
                class="flex items-center gap-2 hover:text-white transition-colors duration-200 group">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"
                  class="text-gray-400 group-hover:text-[#5865F2] transition-colors duration-200">
                  <path
                    d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.419-2.1569 2.419zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.419-2.1568 2.419z" />
                </svg>
                <span>Discord</span>
              </a>
            </li>
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