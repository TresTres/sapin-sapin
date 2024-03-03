export const getUserStore = defineStore("userStore", {
  state: () => ({
    username: "",
    email: "",
    dateJoined: new Date(),
  }),
  persist: {
    storage: persistedState.sessionStorage,
  },
  getters: {
    accountAge(state): number {
      const now = new Date();
      const msPerDay = 1000 * 60 * 60 * 24;
      const dateJoined = new Date(state.dateJoined);
      return (now.getTime() - dateJoined.getTime()) / msPerDay;
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
