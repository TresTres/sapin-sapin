export const useDataStore = defineStore("dataStore", {
  state: () => ({
    isLoading: false as boolean, 
    series: {} as {
      [name: string]: DataEventSeries
    }
  }),
  actions: {
    loadSeries(series: DataEventSeriesResponseObject): void {
      if (series) {
        series.owned_series.forEach((s) => {
          this.series[s.title] = s;
        });
      }
    }
  },
});
