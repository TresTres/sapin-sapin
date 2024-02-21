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


</style>
