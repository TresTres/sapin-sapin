export const getUserStore = defineStore("userStore", {
  state: () => ({
    isLoggedIn: false,
    username: "",
    email: "",
    dateJoined: new Date(),
  }),
  actions: {
    login(user: UserResponseObject) {
      this.isLoggedIn = true;
      this.username = user.username;
      this.email = user.email;
      this.dateJoined = new Date(user.date_joined);
    },
    logout() {
      this.isLoggedIn = false;
      this.username = "";
    },
  },
  getters: {
    getAccountAge(state): number {
      const now = new Date();
      const msPerDay = 1000 * 60 * 60 * 24;
      return Math.abs(now.getTime() - state.dateJoined.getTime()) / msPerDay;
    },
  },
});
