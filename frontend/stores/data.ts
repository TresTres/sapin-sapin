export const useDataStore = defineStore("dataStore", {
  state: () => ({
    allSeries: new Map<string, DataEventSeries>(),
  }),
  actions: {
    addSeries(series: DataEventSeries): void {
      this.allSeries.set(upperCase(series.title), structuredClone(series));
    },
    loadMultipleSeries(setOfSeries: DataEventSeries[]): void {
      if (setOfSeries) {
        setOfSeries.forEach((series: DataEventSeries) => {
          this.allSeries.set(upperCase(series.title), structuredClone(series));
        });
      }
    },
    getSeries(title: string): DataEventSeries | undefined {
      return this.allSeries.get(upperCase(title));
    },
    doesSeriesExist(title: string): boolean {
      return this.allSeries.has(upperCase(title));
    },
    replaceSeries(title: string, series: DataEventSeries): boolean { 
      if(this.doesSeriesExist(title)){
        this.allSeries.set(upperCase(title), structuredClone(series));
        return true;
      }
      return false;
    }
  },
});


const upperCase = (value: any) => String(value).toUpperCase().trim();