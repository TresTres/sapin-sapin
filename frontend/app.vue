<template>
  <header>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/grids-responsive-min.css"
    />
  </header>
  <NuxtLoadingIndicator />
  <NuxtLayout>
    <Navbar
      :routes="[...appRoutes, ...(authStore.loginStatus ? userRoutes : landingRoutes)]"
    />
    <NuxtPage />
  </NuxtLayout>
  <footer></footer>
</template>

<script setup lang="ts">
import "purecss";

const authStore = getAuthStore();

</script>

<style scoped>
header {
  background-color: #671ec1;
}
nav {
  background-color: #671ec1;
}
nav ul {
  list-style-type: none;
  padding: 0;
}
nav ul li {
  display: inline;
  margin-right: 10px;
}
nav ul li a {
  color: white;
  text-decoration: none;
}
footer {
  background-color: #671ec1;
}
</style>
