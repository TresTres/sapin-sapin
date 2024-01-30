<template>
  <div class="pure-menu pure-menu-horizontal">
    <ul class="pure-menu-list navbar-container" v-for="route in routes">
        <li class="pure-menu-item">
            <NuxtLink class="pure-menu-link navbar-link" :to="`/${route.path}`">{{route.name}}</NuxtLink>
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

<style scoped>

.navbar-container {
    background-color: #671ec1;
    list-style-type: none;
    padding: 0;
 }
 .navbar-link {
    color: white;
    text-decoration: none;
 }
</style>
