<template>
  <div class="app-container">
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <template #header>
        <Navbar
          :routes="[...appRoutes, ...(userStore.loginStatus ? userRoutes : landingRoutes)]"
        />
      </template>
      <NuxtPage />
      <template #footer>
        <div>Footer</div>
      </template>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import "purecss";

const userStore = getUserStore();

</script>

<style lang="scss" scoped>

.app-container {
  height: 100%;
  background-color: $light-color;
  margin: 0;
  padding: 0;
}

</style>
