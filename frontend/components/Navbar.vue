<template>
  <div class="navbar-container">
    <ul class="navbar-list">
      <li v-for="route in routes" class="navbar-item">
        <div class="link-container"> 
          <NuxtLink class="navbar-link" :to="`/${route.path}`">{{
            route.name
          }}</NuxtLink>
        </div>
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
  display: flex;
  flex-direction: column;

  max-width: 20%;
  height: 100vh;

  background-color: $dark-purple-color;

  box-shadow:
      4px 0px 12px 0 rgba(0, 0, 0, 0.2),
      8px 0px 24px 0 rgba(0, 0, 0, 0.19);
      
  li {


    list-style: none;
    .link-container {
      padding: .5rem 2rem;

      .navbar-link {
        text-decoration: none;
        color: $light-purple-color;
        font-size: $medium-text-size;
      }
    }
    :hover {
        background-color: $primary-purple-color;
      }
  }

}
</style>
