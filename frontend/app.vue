<template>
  <div class="app-container">
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <template #header>
        <div>Header</div>
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
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: $light-color;
}

</style>
