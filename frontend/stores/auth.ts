export const getAuthStore = defineStore("authStore", {


  state: () => ({
    isLoggedIn: false as boolean,
    authError: "" as string,
    bearerToken: "" as string,
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
          await navigateTo("/");
        })
        .catch((error): void => {
          this.logout(error.message);
        });
    },
    async logout(errorMessage?: string): Promise<void>{
      const userStore = getUserStore();
      userStore.logout();
      this.isLoggedIn = false;
      this.bearerToken = "";
      this.authError = errorMessage || "";
      useCookie("refresh_token").value = null;
    },
  },
});
