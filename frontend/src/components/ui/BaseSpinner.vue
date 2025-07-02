<template>
    <div aria-label="Loading" class="spinner"></div>
  </template>
  
  <style scoped>
  .spinner {
    width: 1.25rem; /* 20px */
    height: 1.25rem; /* 20px */
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  </style>