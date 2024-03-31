export const useDataStore = defineStore("dataStore", {
  state: () => ({
    allSeries: new Map<string, DataEventSeries>(),
  }),
  actions: {
    addSeries(series: DataEventSeries): void {
      this.allSeries.set(lowerCase(series.title), structuredClone(series));
    },
    loadMultipleSeries(setOfSeries: DataEventSeries[]): void {
      if (setOfSeries) {
        setOfSeries.forEach((series: DataEventSeries) => {
          this.allSeries.set(lowerCase(series.title), structuredClone(series));
        });
      }
    },
    getSeries(title: string): DataEventSeries | undefined {
      return this.allSeries.get(lowerCase(title));
    },
    doesSeriesExist(title: string): boolean {
      return this.allSeries.has(lowerCase(title));
    },
    replaceSeries(title: string, series: DataEventSeries): boolean { 
      if(this.doesSeriesExist(title)){
        this.allSeries.set(lowerCase(title), structuredClone(series));
        return true;
      }
      return false;
    }
  },
});


const lowerCase = (value: any) => String(value).toLowerCase().trim();