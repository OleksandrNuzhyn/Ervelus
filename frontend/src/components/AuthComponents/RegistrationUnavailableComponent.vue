<template>
  <div class="form-container space-y-6 text-center">
    <h2 class="text-3xl font-bold text-white">Registration is currently unavailable</h2>
    <p class="mt-2 text-gray-300">
      We apologize for the inconvenience. Our registration process is temporarily closed.
      Please check back later or log in if you already have an account
    </p>
    <router-link
      to="/login"
      class="block w-full py-3 font-bold text-gray-800 transition duration-300 rounded-md bg-white/60 backdrop-blur-md border border-white/20 shadow-lg hover:bg-white/20 hover:text-white"
    >
      Log in
    </router-link>
  </div>
</template>

<style scoped>
.form-container {
  height: 100%;
  margin-left: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: rgba(10, 10, 10, 0.3) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 2rem;
  font-family: 'Manrope', sans-serif;
  color: #e5e7eb;
  mask-image: radial-gradient(ellipse at center, black 50%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 65%, transparent 100%);
}
</style>