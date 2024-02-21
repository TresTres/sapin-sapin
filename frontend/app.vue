<template>
  <div class="app-container">
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <div v-if="userStore.loginStatus">
        <Navbar
          :routes="appRoutes"
        />
      </div>
      <div v-else>
        <LandingCard />
      </div>
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
