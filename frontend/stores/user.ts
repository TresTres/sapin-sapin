export const getUserStore = defineStore("userStore", {
  state: () => ({
    username: "",
    email: "",
    dateJoined: JSON.stringify(new Date()),
  }),
  persist: {
    storage: persistedState.sessionStorage,
  },
  getters: {
    accountAge(state): number {
      const now = new Date();
      const msPerDay = 1000 * 60 * 60 * 24;
      const dateJoined = Date.parse(state.dateJoined);
      return Math.abs(now.getTime() - dateJoined) / msPerDay;
    },
  },
  actions: {
    login(user: UserResponseObject) {
      this.username = user.username;
      this.email = user.email;
      this.dateJoined = JSON.stringify(new Date(user.date_joined));
    },
    logout() {
      this.$reset();
    },
  },
});
