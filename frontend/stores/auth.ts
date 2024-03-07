import type { SimplifiedApiResponseObject } from "~/server/utils";
import type { UserResponseObject } from "~/utils/interfaces/response-objects";

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
      await useFetch("/api/login", {
        method: "POST",
        body: JSON.stringify({
          identifier: identifier,
          password: password,
        }),
      }).then(
        async ({ data: { value } }):  Promise<void> => {
          const { headers, payload, error } = value as SimplifiedApiResponseObject;
          if(error) {
            this.clearAuth();
            if(error.value.statusCode === 401) {
              this.authError = "Invalid username or password";
            } else {
              this.authError = "An unspecified error occurred";
            }
            return;
          }
          this.accessToken = headers.get("Authorization") || "";
          this.isLoggedIn = true;
          this.authError = "";
          this.accessToken = headers.get("Authorization") || "";
          const userStore = useUserStore();
          userStore.fillData(payload?.user as UserResponseObject);
          await navigateTo("/");
        }
      )
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
