<template>
  <div class="app-container">
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <template #header>
        <Navbar :routes="appRoutes" />
      </template>
      <NuxtPage />
      <template #footer>
        <div>Footer Text</div>
      </template>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">

const authStore = getAuthStore();
</script>

<style lang="scss" scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;

  background-color: $dark-color;
}
</style>
