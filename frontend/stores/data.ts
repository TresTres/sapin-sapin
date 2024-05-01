export const useDataStore = defineStore("dataStore", {
  state: () => ({
    allSeries: {} as {
      [key: string]: DataEventSeries;
    }
  }),
  persist: {
    storage: persistedState.sessionStorage,
  },
  actions: {
    addSeries(series: DataEventSeries): void {
      this.allSeries[lowerCase(series.title)] = structuredClone(series);
    },
    loadMultipleSeries(setOfSeries: DataEventSeries[]): void {
      if (setOfSeries) {
        setOfSeries.forEach((series: DataEventSeries) => {
          this.allSeries[lowerCase(series.title)] = structuredClone(series);
        });
      }
    },
    getSeries(title: string): DataEventSeries | null {
      if(this.allSeries.hasOwnProperty(lowerCase(title))){
        return this.allSeries[lowerCase(title)];
      }
      return null;
    },
    has(title: string): boolean {
      return this.allSeries.hasOwnProperty(lowerCase(title));
    },
    replaceSeries(title: string, series: DataEventSeries): boolean { 
      if(this.has(title)){

        this.allSeries[lowerCase(title)] = structuredClone(series);
        return true;
      }
      return false;
    }
  },
  getters: {
    allSeriesEntries: (state) => Object.entries(state.allSeries)
  }
});

const lowerCase = (value: any) => String(value).toLowerCase().trim();