import type { RouteLocationNormalized } from "vue-router";

export default defineNuxtRouteMiddleware((to: RouteLocationNormalized, from) => {

  if (process.server) {
    if(!useCookie("refresh_token")) {
      return navigateTo("/login");
    }
    return;
  }

  const authStore = getAuthStore();
  if (!authStore.isLoggedIn && to.path !== "/login") {
    return navigateTo("/login");
  }
});
