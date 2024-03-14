<template>
  <div class="navbar-container">
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
</script>

<style lang="scss" scoped>
.navbar-container {
  display: flex;
  flex-direction: column;

  max-width: 10%;
  height: 100vh;

  background-color: $dark-purple-color;

}
</style>
