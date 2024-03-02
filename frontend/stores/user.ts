export const getUserStore = defineStore("userStore", {
  state: () => ({
    username: "",
    email: "",
    dateJoined: new Date(),
  }),
  getters: {
    getAccountAge(state): number {
      const now = new Date();
      const msPerDay = 1000 * 60 * 60 * 24;
      return Math.abs(now.getTime() - state.dateJoined.getTime()) / msPerDay;
    },
  },
  actions: {
    login(user: UserResponseObject) {
      this.username = user.username;
      this.email = user.email;
      this.dateJoined = new Date(user.date_joined);
    },
    logout() {
      this.$reset();
    },
  },
});
