
export const getAuthStore = defineStore('authStore', {
    state: () => ({
      isLoggedIn: false as boolean, 
      authError: '' as string, 
    }),
    actions: {
    

        async login(identifier: string, password: string): Promise<void> {
            await useBaseFetch("/login", {
                method: "POST",
                body: JSON.stringify({
                  identifier: identifier,
                  password: password,
                }),
              })
            .then(async ({ data, error }): Promise<void> => {
                const errorContent = error.value
                if (errorContent) {
                    if (errorContent?.statusCode === 401) {
                        throw new Error("Invalid username or password")
                    } else {
                        throw new Error("An error occurred")
                    }
                }
                const { user } = data?.value as { user: UserObject }
                const userStore = getUserStore()
                userStore.fillUser(user)
                this.isLoggedIn = true
                this.authError = 'Login successful'
                await navigateTo("/")
            })
            .catch((error) => {
                const userStore = getUserStore()
                userStore.clear()
                this.authError = error.message
            });
        },
        async logout(): Promise<void> {
            this.isLoggedIn = false
            this.authError = ''
            await navigateTo("/login")
        }
    },
    getters: {
        loginStatus(state): boolean {
            return state.isLoggedIn
        },
        getAuthError(state): string {
            return state.authError
        }
    }
  });