import type { RouteLocationNormalized } from "vue-router";

export default defineNuxtRouteMiddleware((to: RouteLocationNormalized) => {
  const authStore = getAuthStore();

  if (!authStore.isLoggedIn && to.path !== "/login") {
    return navigateTo("/login");
  }
});
