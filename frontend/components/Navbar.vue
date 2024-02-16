<template>
    <div class="navbar-container">
        <ul class="navbar-list" >
            <li class="navbar-item" v-for="route in routes">
                <NuxtLink class="navbar-link" :to="`/${route.path}`">{{route.name}}</NuxtLink>
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
    height: 6vh;


    background-color: $primary-purple-color;
}


.navbar-list {

    width: 80%;
    height: 100%;
    padding: 0;
    margin: auto;

    list-style: none;
    display: flex;
    justify-content: space-around;
    align-items: center;

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
