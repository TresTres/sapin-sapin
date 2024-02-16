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

const userStore = getUserStore();

</script>
