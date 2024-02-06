export const getUserStore = defineStore('userStore', {
    state: () => ({
      isLoggedIn: false, 
      username: '',
    }),
    actions: {
        login(username: string) {
            this.isLoggedIn = true
            this.username = username
        },
        logout() {
            this.isLoggedIn = false
            this.username = ''
        }
    },
    getters: {
        loginStatus(state): boolean {
            return state.isLoggedIn
        },
    }
  })