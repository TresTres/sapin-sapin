<template>
  <aside class="navbar-container">
    <ul class="navbar-list">
      <li v-for="route in routes" class="navbar-item">
        <NuxtLink class="navbar-link" :to="`/${route.path}`">
          <div class="link-container">
            {{ route.name }}
          </div>
        </NuxtLink>
      </li>
    </ul>
  </aside>
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

    background-color: $light-purple-color;

    box-shadow:
      4px 0px 12px 0 rgba(0, 0, 0, 0.2),
      8px 0px 24px 0 rgba(0, 0, 0, 0.19);

    li {
      list-style: none;
      .navbar-link {
        text-decoration: none;
        color: $primary-purple-color;
        font-size: $medium-large-text-size;
        letter-spacing: .05em;
        
        .link-container {
          padding: 1rem 2rem;
        }
      
      }
      :hover {
        background-color: $primary-purple-color;
        color: $white-color;
      }
    }
  }
</style>
