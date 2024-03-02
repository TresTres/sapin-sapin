export const getAuthStore = defineStore("authStore", {


  state: () => ({
    isLoggedIn: false as boolean,
    authError: "" as string,
    bearerToken: "" as string,
  }),
  persist: {
    paths: ["isLoggedIn", "bearerToken"],
    storage: persistedState.sessionStorage,
  },
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
        .catch((error): void => {
          this.logout(error.message);
        });
    },
    logout(errorMessage?: string): void {
      const userStore = getUserStore();
      userStore.logout();
      this.isLoggedIn = false;
      this.authError = errorMessage || "";
      // ensure navigation to the login page
    },
  },
});
