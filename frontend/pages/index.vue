<template>
  <h1>Example</h1>
</template>



<script setup lang="ts">
definePageMeta({
    title: "Profile Page",
    layout: "dashboard"
});

const userStore = getUserStore()
</script>

<style lang="scss" scoped>
h1 {
  color: red;
}
</style>