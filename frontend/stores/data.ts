import { useAuthorizingFetch } from "~/composables/authorizingFetch";

export const getDataStore = defineStore("dataStore", {
  state: () => ({
    isLoading: false as boolean, 
    series: {} as {
      [name: string]: DataEventSeries
    }
  }),
  actions: {
    // async createSeries()
    async loadForUser() {
      this.isLoading = true;
      await useAuthorizingFetch(
        "api/data/series", 
      ).then(({ data }) => {
        const series = data?.value as DataEventSeriesResponseObject;
        if (series) {
          series.owned_series.forEach((s) => {
            this.series[s.title] = s;
          });
        }
        this.isLoading = false;
      });
    }
  },
});
