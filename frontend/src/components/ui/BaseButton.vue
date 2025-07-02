<template>
    <button :type="type" :disabled="disabled || isLoading" class="relative flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-purple-600 border border-transparent rounded-md group hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:bg-purple-300 disabled:cursor-not-allowed">
      <span class="absolute inset-y-0 left-0 flex items-center pl-3">
        <BaseSpinner v-if="isLoading" />
      </span>
      <slot />
    </button>
  </template>
  
  <script setup>
  import BaseSpinner from './BaseSpinner.vue';
  defineProps({
    type: { type: String, default: 'submit' },
    disabled: Boolean,
    isLoading: Boolean,
  });
  </script>