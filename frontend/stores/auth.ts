import type { FetchResponse, FetchError } from 'ofetch';

export const useAuthStore = defineStore("authStore", {
  state: () => ({
    accessToken: "" as string,
    isLoggedIn: false as boolean,
    authError: "" as string,
  }),
  persist: {
    storage: persistedState.sessionStorage,
    paths: ["isLoggedIn"]
  },
  actions: {
    async login(identifier: string, password: string): Promise<void> {
      await $fetch.raw("/api/login", {
        method: "POST",
        body: JSON.stringify({
          identifier: identifier,
          password: password,
        }),
      }).then(
        async (resp: FetchResponse<any>):  Promise<void> => {
          const { headers,  _data: { user } } = resp;
          this.isLoggedIn = true;
          this.authError = "";
          this.accessToken = headers.get("Authorization") || "";
          const userStore = useUserStore();
          userStore.fillData(user as UserResponseObject);
          await navigateTo("/");
        }
      ).catch((error: FetchError): void => {
        this.clearAuth();
        if(error.status === 401) {
          this.authError = "Invalid username or password.";
        } else {
          this.authError = "An error occurred on login.  Please retry again later.";
          console.error(error.data);
        }
        return;
      })
    },
    async refreshAuth(): Promise<void> {
      await useFetch("/api/token", {
        method: "GET",        
        onResponse: ({ response }): void => {
          this.accessToken = response.headers.get("Authorization") || "";
        },
      }).then(async ({ data, error }): Promise<void> => {
        const errorContent = error.value;
        if (errorContent) {
          if (errorContent?.statusCode === 401) {
            throw new Error("Invalid refresh token");
          } else {
            throw new Error("An error occurred");
          }
        }
        const { user } = data?.value as { user: UserResponseObject };
        const userStore = useUserStore();
        userStore.login(user);
        this.isLoggedIn = true;
      }).catch((error): void => {
        this.clearAuth(error.message);
      });
    },
    clearAuth(): void{
      const userStore = useUserStore();
      userStore.clearData();
      this.isLoggedIn = false;
    },
  },
});
