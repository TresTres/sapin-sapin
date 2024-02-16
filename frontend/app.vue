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

<style lang="scss" scoped>


.app-container {

  margin: 0;
  padding: 0;

  background-color: $primary-yellow-color;
}

</style>
