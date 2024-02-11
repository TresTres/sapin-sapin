export const getUserStore = defineStore('userStore', {
    state: () => ({
      username: '' as string,
      email: '' as string, 
      dateJoined: new Date() as Date,
    }),
    actions: {
        fillUser(user: UserObject) {
            this.username = user.username
            this.email = user.email
            this.dateJoined = new Date(user.date_joined)
        },
        
        clear() {
            this.username = ''
            this.email = ''
            this.dateJoined = new Date()
        }
    },
    getters: {
        getUsername(state): string {
            return state.username
        },
        getEmail(state): string {
            return state.email
        },
        getAccountAge(state): number {
            const now = new Date()
            const msPerDay = 1000 * 60 * 60 * 24
            return Math.abs(now.getTime() - state.dateJoined.getTime()) / msPerDay
        }
    }
  })