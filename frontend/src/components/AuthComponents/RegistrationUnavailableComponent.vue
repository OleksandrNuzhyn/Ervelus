<template>
  <div class="form-container space-y-8 text-center">
    <div class="space-y-4">
      <h2 class="text-3xl font-bold text-white">Registration is currently unavailable</h2>
      <p class="text-gray-400 text-sm leading-relaxed max-w-sm mx-auto">
        We apologize for the inconvenience. Our registration process is temporarily closed
      </p>
    </div>

    <div class="pt-4">
      <router-link
        to="/login"
        class="block w-full py-3 font-bold text-gray-800 transition duration-300 rounded-md bg-gray-400 border border-gray-500 shadow-lg hover:bg-gray-500 hover:text-gray-900"
      >
        Sign In
      </router-link>
    </div>
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
}
</style>