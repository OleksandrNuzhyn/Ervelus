<template>
  <button @click="redirectToCustomerPortal" class="portal-button" :disabled="isLoading">
    Manage Billing
  </button>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';

const isLoading = ref(false);

const redirectToCustomerPortal = async () => {
  isLoading.value = true;

  try {
    const response = await api.post('api/subscriptions/customer-portal/');
    const portalUrl = response.data.portal_url;
    if (portalUrl) {
      window.location.href = portalUrl;
    }
    else {
      console.error('Customer portal URL not found in response:', response);
    }
  }
  catch (error) {
    console.error('Error creating customer portal session:', error);
  }
 
  finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.portal-button {
  background-color: white;
  color: black;
  border: 1px solid black;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
}

.portal-button:disabled {
  background-color: #f0f0f0;
  color: #ccc;
  cursor: not-allowed;
  border-color: #ccc;
}
</style>
