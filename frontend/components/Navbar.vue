<template>
  <div v-show="authStore.isLoggedIn" class="navbar-container">
    <ul class="navbar-list">
      <li v-for="route in routes" class="navbar-item">
        <NuxtLink class="navbar-link" :to="`/${route.path}`">{{
          route.name
        }}</NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
const { routes } = defineProps<{
  routes: {
    name: string;
    path: string;
  }[];
}>();

const authStore = getAuthStore();
</script>

<style lang="scss" scoped>
.navbar-container {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
}
</style>
