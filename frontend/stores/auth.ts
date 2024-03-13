import type { FetchResponse, FetchError } from 'ofetch';

export const useAuthStore = defineStore("authStore", {
  state: () => ({
    accessToken: "" as string,
    isLoggedIn: false as boolean,
    authError: "" as string,
    
  }),
  persist: {
    storage: persistedState.localStorage,
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
          this.accessToken = headers.get("Authorization")?.split(" ")[1] || "";
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
    clearAuth(): void{
      const userStore = useUserStore();
      userStore.clearData();
      this.isLoggedIn = false;
    }
  },
});
