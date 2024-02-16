<template>
  <div class="header-container">
    <div class="navbar-container">
        <ul class="pure-menu-list" >
            <li class="pure-menu-item navbar-item" v-for="route in routes">
                <NuxtLink class="pure-menu-link navbar-link" :to="`/${route.path}`">{{route.name}}</NuxtLink>
            </li>
        </ul>
    </div>
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
    height: 6vh;
    list-style-type: none;
 

    background-color: $primary-purple-color;

 }
 .navbar-link {

    color: $light-color;
    text-decoration: none;
    font-size: 1.1rem;


 }

 pure-menu-selected {
    background-color: $secondary-purple-color;
}
</style>
