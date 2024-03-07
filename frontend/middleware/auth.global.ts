import type { RouteLocationNormalized } from "vue-router";

export default defineNuxtRouteMiddleware((to: RouteLocationNormalized) => {

  if (process.server) {
    const refreshToken = useCookie("refresh_token");
    if(!refreshToken.value && to.path !== "/login") {
      return navigateTo("/login");
    }
    return;
  }

  const authStore = useAuthStore();
  if (!authStore.isLoggedIn && to.path !== "/login") {
    return navigateTo("/login");
  }
});
