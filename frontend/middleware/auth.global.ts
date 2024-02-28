import type { RouteLocationNormalized } from "vue-router";

export default defineNuxtRouteMiddleware((to: RouteLocationNormalized) => {

  const userStore = getUserStore();

  if (!userStore.isLoggedIn && to.path !== '/login') {
    return navigateTo('/login');
  }
});