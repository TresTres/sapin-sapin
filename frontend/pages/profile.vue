
<template>
  <div>
    <h1>Profile</h1>
    <p>Username: {{ userStore.getUsername }}</p>
    <p>Email: {{ userStore.getEmail }}</p>
    <p>Account age: {{ userStore.getAccountAge.toFixed(2) }} days</p>
    <button
      class="pure-button pure-input-1-2 pure-button-primary"
      @click="authStore.logout"
    >
      Logout
    </button>
  </div>
</template>

<script setup lang="ts">
const authStore = getAuthStore();
const userStore = getUserStore();
</script>
