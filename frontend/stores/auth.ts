import type {
  RouteLocationNormalized,
} from "vue-router";

export const getAuthStore = defineStore("authStore", {


  state: () => ({
    isLoggedIn: false as boolean,
    authError: "" as string,
    bearerToken: useSessionStorage("Bearer Token", "" as string),
  }),
  actions: {
    async login(identifier: string, password: string): Promise<void> {
      await useBaseFetch("/login", {
        method: "POST",
        body: JSON.stringify({
          identifier: identifier,
          password: password,
        }),
        onResponse: ({ response }): void => {
          
          this.bearerToken = response.headers.get("Authorization") || "";
        },
      })
        .then(async ({ data, error }): Promise<void> => {
          const errorContent = error.value;
          if (errorContent) {
            if (errorContent?.statusCode === 401) {
              throw new Error("Invalid username or password");
            } else {
              throw new Error("An error occurred");
            }
          }
          const { user } = data?.value as { user: UserResponseObject };
          const userStore = getUserStore();
          userStore.login(user);
          this.isLoggedIn = true;
          this.authError = "";
          // ensure navigation to the home page
          await navigateTo("/");
        })
        .catch(async (error): Promise<void> => {
          await this.logout(error.message);
        });
    },
    async logout(errorMessage?: string): Promise<void> {
      const userStore = getUserStore();
      userStore.logout();
      this.isLoggedIn = false;
      this.authError = errorMessage || "";
      this.bearerToken = "";
      // ensure navigation to the login page
      await navigateTo("/login");
    },
    async rehydrate(to: RouteLocationNormalized): Promise<void> {
      if (this.bearerToken !== "") {
        await useBaseFetch("/login", {
          method: "GET",
        })
          .then(async ({ data }): Promise<void> => {
            const { user } = data?.value as { user: UserResponseObject };
            const userStore = getUserStore();
            userStore.login(user);
            this.isLoggedIn = true;
            this.authError = "";
            await navigateTo(to.path);
          })
          .catch(async (error): Promise<void> => {
            await this.logout(error.message);
          });
      }
      await this.logout();
    },
  },
});
