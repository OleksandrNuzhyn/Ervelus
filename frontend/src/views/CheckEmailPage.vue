<template>
  <AuthLayout>
    <div class="text-center">
      <h2 class="text-3xl font-extrabold text-gray-100">Перевірте вашу пошту</h2>
      <p class="mt-4 text-gray-400">
        Ми надіслали вам лист з посиланням для підтвердження вашого акаунту. Будь ласка, перейдіть за ним, щоб завершити реєстрацію.
      </p>
      <div class="mt-8">
        <RouterLink to="/login" class="font-medium text-purple-400 hover:text-purple-300">
          Повернутися на сторінку входу
        </RouterLink>
      </div>
    </div>
  </AuthLayout>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import AuthLayout from '@/layouts/AuthLayout.vue';
</script>