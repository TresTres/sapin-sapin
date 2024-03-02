<template>
  <div>
    <h1>Profile</h1>
    <p>Username: {{ userStore.getUsername }}</p>
    <p>Email: {{ userStore.getEmail }}</p>
    <p>Account age: {{ userStore.getAccountAge.toFixed(2) }} days</p>
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
const router = useRouter();

const logout = (): void => {
  userStore.logout();
};
</script>
