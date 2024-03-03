import type { RouteLocationNormalized } from "vue-router";

export default defineNuxtRouteMiddleware((to: RouteLocationNormalized, from) => {

  if (process.server) {
    console.log("Server side navigation, skipping auth check")
    return 
  } 
  const authStore = getAuthStore();
  if (!authStore.isLoggedIn && to.path !== "/login") {
    return navigateTo("/login");
  }
});
