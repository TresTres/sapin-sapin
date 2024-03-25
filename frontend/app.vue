import { ServerPlaceholder } from './.nuxt/components';
<template>
  <div class="app-container">
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">


</script>

<style lang="scss" scoped>


.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;

  background-color: $primary-purple-color;

  font-family: "Rubik", Roboto, sans-serif;
}
</style>
