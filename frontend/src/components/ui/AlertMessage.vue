<template>
    <div v-if="message" :class="alertClasses">
      <p>{{ message }}</p>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  
  const props = defineProps({
    message: String,
    type: {
      type: String,
      default: 'success',
    },
  });
  
  const alertClasses = computed(() => [
    'p-4',
    'rounded-md',
    'text-sm',
    {
      'bg-green-50 text-green-800': props.type === 'success',
      'bg-red-50 text-red-800': props.type === 'error',
    }
  ]);
  </script>