<template>
  <Teleport to="body">
    <transition name="modal-fade">
      <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center" role="dialog">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-md transition-opacity" @click="$emit('close')"></div>
        <div class="relative w-full max-w-lg md:max-w-xl h-auto max-h-[85vh] m-4 bg-[#1c1c1e]/80 backdrop-blur-xl border border-white/[0.02] rounded-2xl overflow-hidden flex flex-col shadow-2xl z-10 transition-all">
          <div class="px-6 py-6 flex items-center justify-between shrink-0">
            <h2 class="text-xl font-bold text-white tracking-tight inter">Store</h2>
            <button @click="$emit('close')" class="p-2 text-white/50 hover:text-white transition-colors">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto px-6 pb-10 space-y-10 no-scrollbar">
            <section>
              <h3 class="text-sm font-medium text-white/60 mb-4 text-center inter">Free Bonuses</h3>
              <div class="flex gap-3">
                
                <button class="relative flex-1 min-w-0 h-[160px] rounded-2xl p-5 flex flex-col justify-between items-start bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.05] transition-all group text-left active:scale-95 shadow-lg overflow-hidden">
                  <div class="absolute -right-4 -top-4 w-24 h-24 bg-white/[0.02] rounded-full blur-2xl pointer-events-none group-hover:bg-white/[0.05] transition-colors"></div>
                  
                  <div class="mb-2 group-hover:scale-110 transition-transform duration-300">
                    <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                  </div>
                  <div class="relative z-10">
                    <span class="block text-4xl font-bold text-white mb-1 tracking-tighter inter">+2</span>
                    <span class="text-xs font-medium text-white/50 leading-tight block inter">Invite friend</span>
                  </div>
                </button>

                <button class="relative flex-1 min-w-0 h-[160px] rounded-2xl p-5 flex flex-col justify-between items-start bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.05] transition-all group text-left active:scale-95 shadow-lg overflow-hidden">
                   <div class="absolute -right-4 -top-4 w-24 h-24 bg-blue-500/[0.02] rounded-full blur-2xl pointer-events-none group-hover:bg-blue-500/[0.05] transition-colors"></div>

                    <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                       <path d="M21.928 2.528c-.03-.213-.206-.386-.418-.415-.178-.025-.36.02-.505.115L1.87 10.42c-.25.13-.393.41-.365.69.027.28.232.506.508.56l4.63 1.07 10.66-6.68c.05-.03.11-.002.115.056.006.06-.05.105-.1.134l-8.6 7.62v3.65c0 .22.14.417.346.502.07.03.144.045.217.045.148 0 .29-.07.39-.19l2.74-3.35 4.88 3.55c.13.093.287.142.443.142.067 0 .135-.01.202-.027.22-.058.388-.23.447-.45l3.235-15.17c.046-.22-.04-.445-.205-.59z"/>
                    </svg>
                  <div class="relative z-10">
                    <span class="block text-4xl font-bold text-white mb-1 tracking-tighter inter">+2</span>
                    <span class="text-xs font-medium text-white/50 leading-tight block inter">Join channel</span>
                  </div>
                </button>
              </div>
            </section>

            <section>
               <h3 class="text-sm font-medium text-white/60 mb-4 text-center inter">Star Packages</h3>
               <div class="flex flex-col gap-3">
                  <div class="group bg-white/[0.03] hover:bg-white/[0.06] border border-white/[0.05] rounded-2xl p-4 flex items-center gap-4 transition-all active:scale-[0.99] cursor-pointer">
                     <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-white/90 group-hover:bg-white/10 transition-colors shrink-0 border border-white/5">
                        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>
                     </div>
                     <div class="flex-1 min-w-0 flex flex-col items-start gap-0.5">
                        <h4 class="text-lg font-bold text-white tracking-tight inter">25 Photos</h4>
                        <p class="text-[11px] text-white/50 font-medium inter leading-tight">Unlock all premium styles</p>
                     </div>
                     <button class="shrink-0 h-10 px-5 bg-white text-black text-sm font-bold rounded-xl hover:bg-gray-100 transition-colors inter whitespace-nowrap flex items-center gap-1.5 ml-auto">
                        199 
                        <svg class="w-3.5 h-3.5 text-yellow-500 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21z"/></svg>
                     </button>
                  </div>

                  <div class="relative group bg-white/[0.07] border border-white/10 rounded-2xl p-4 transition-all active:scale-[0.99] cursor-pointer shadow-[0_0_30px_rgba(59,130,246,0.15)] overflow-hidden">
                     <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-blue-500/10 opacity-100"></div>
                     <div class="flex items-center gap-4 relative z-10">
                        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center text-white border border-white/10 shrink-0">
                           <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                        </div>
                        <div class="flex-1 min-w-0 flex flex-col items-start gap-0.5">
                           <h4 class="text-lg font-bold text-white tracking-tight inter">50 Photos</h4>
                           <p class="text-[11px] text-white/50 font-medium inter leading-tight">Unlock all premium styles</p>
                        </div>
                        <button class="shrink-0 h-10 px-5 bg-white text-black text-sm font-bold rounded-xl hover:bg-gray-200 transition-colors shadow-[0_0_15px_rgba(255,255,255,0.3)] inter whitespace-nowrap flex items-center gap-1.5 ml-auto">
                           349 
                           <svg class="w-3.5 h-3.5 text-yellow-500 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21z"/></svg>
                        </button>
                     </div>
                  </div>

                  <div class="group bg-white/[0.03] hover:bg-white/[0.06] border border-white/[0.05] rounded-2xl p-4 flex items-center gap-4 transition-all active:scale-[0.99] cursor-pointer">
                     <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-white/90 group-hover:bg-white/10 transition-colors shrink-0 border border-white/5">
                        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                     </div>
                     <div class="flex-1 min-w-0 flex flex-col items-start gap-0.5">
                        <h4 class="text-lg font-bold text-white tracking-tight inter">100 Photos</h4>
                        <p class="text-[11px] text-white/50 font-medium inter leading-tight">Unlock all premium styles</p>
                     </div>
                     <button class="shrink-0 h-10 px-5 bg-white text-black text-sm font-bold rounded-xl hover:bg-gray-100 transition-colors inter whitespace-nowrap flex items-center gap-1.5 ml-auto">
                        599 
                        <svg class="w-3.5 h-3.5 text-yellow-500 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21z"/></svg>
                     </button>
                  </div>

               </div>
            </section>
            <div class="pb-10"></div>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
defineProps({
  isOpen: Boolean
});

defineEmits(['close']);
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>