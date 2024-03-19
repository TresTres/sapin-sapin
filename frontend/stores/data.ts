export const useDataStore = defineStore("dataStore", {
  state: () => ({
    allSeries: new Map<string, DataEventSeries>(),
  }),
  actions: {
    loadMultipleSeries(series: DataEventSeries[]): void {
      if (series) {
        series.forEach((s: DataEventSeries) => {
          this.allSeries.set(upperCase(s.title), s);
        });
      }
    },
    addSeries(series: DataEventSeries): void {
      this.allSeries.set(upperCase(series.title), series);
    },
    replaceSeries(series: DataEventSeries): void { 
      if(this.doesSeriesExist(series.title)){
        this.allSeries.set(upperCase(series.title), series);
      }
    },
    doesSeriesExist(title: string): boolean {
      return this.allSeries.has(upperCase(title));
    },
  },
});


const upperCase = (value: any) => String(value).toUpperCase().trim();