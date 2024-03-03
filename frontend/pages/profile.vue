<template>
  <div>
    <h1>Profile</h1>
    <p>Username: {{ username }}</p>
    <p>Email: {{ email }}</p>
    <p>Account age: {{ accountAge.toFixed(2) }} days</p>
    <button
      class="pure-button pure-input-1-2 pure-button-primary"
      @click="logout"
    >
      Logout
    </button>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "dashboard",
});
const userStore = getUserStore();
const authStore = getAuthStore();
const { username , email,  accountAge } = storeToRefs(userStore);

const logout = async(): Promise<void> => {
  authStore.logout();
  await navigateTo("/login");
};
</script>
