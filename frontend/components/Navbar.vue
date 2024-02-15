<template>
  <div class="pure-menu pure-menu-horizontal navbar-container">
    <ul class="pure-menu-list" v-for="route in routes">
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

<style lang="scss" scoped>

.navbar-container {
    width: 100%;
    background-color: $primary-purple-color;
    list-style-type: none;
    padding: 0;
 }
 .navbar-link {
    color: $light-color;
    text-decoration: none;

 }
</style>
