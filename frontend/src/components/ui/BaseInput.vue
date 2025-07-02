<template>
    <div>
      <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700">{{ label }}</label>
      <div class="mt-1">
        <input
          :id="id"
          :type="type"
          :placeholder="placeholder"
          :required="required"
          v-model="model"
          class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          :class="{ 'border-red-500': error }"
        />
      </div>
      <p v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  defineProps({
    id: String,
    label: String,
    type: { type: String, default: 'text' },
    placeholder: String,
    required: Boolean,
    error: String,
  });
  const model = defineModel();
  </script>