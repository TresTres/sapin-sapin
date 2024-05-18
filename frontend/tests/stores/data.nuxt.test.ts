import { setActivePinia, createPinia } from "pinia";
import { describe, beforeEach, beforeAll, it, expect } from "vitest";

import type { DataEventSeries } from "@/utils/interfaces/state-objects";

describe("Financial Data Store", () => {
  let seriesToAdd: DataEventSeries;
  let seriesToAdd2: DataEventSeries;
  let data: ReturnType<typeof useDataStore>;
  beforeAll(() => {
    seriesToAdd = {
      id: "1",
      title: "Test Series",
      description: "A test series",
      events: [],
      recurrences: [],
    };
    seriesToAdd2 = {
      id: "2",
      title: "Test Series 2",
      description: "Another test series",
      events: [],
      recurrences: [],
    };
  });
  beforeEach(() => {
    setActivePinia(createPinia());
    data = useDataStore();
  });
  it("can add add a data series", () => {
    expect(data.allSeries.size).toBe(0);
    data.addSeries(seriesToAdd);
    expect(data.allSeries.size).toBe(1);
    expect(data.allSeries.values().next().value).toEqual(seriesToAdd);
  });
  it("can retrieve stored series with case-insensitive title", () => {
    data.addSeries(seriesToAdd);
    const retrievedSeries = data.getSeries("teSt sEries");
    expect(retrievedSeries).toEqual(seriesToAdd);
  });
  it("can load multlpie data series", () => {
    data.loadMultipleSeries([seriesToAdd, seriesToAdd2]);
    expect(data.allSeries.size).toBe(2);
    expect(data.allSeries.get("TEST SERIES")).not.toBeUndefined();
    expect(data.allSeries.get("TEST SERIES 2")).not.toBeUndefined();
  });
  it("maintains the most recent addition when loading multiple data series with the same title", () => {
    seriesToAdd2.title = "Test Series";
    data.loadMultipleSeries([seriesToAdd, seriesToAdd2]);
    expect(data.allSeries.size).toBe(1);
    expect(data.allSeries.values().next().value).toEqual(seriesToAdd2);
  });
  it("can replace an existing series", () => {
    data.addSeries(seriesToAdd);
    expect(data.replaceSeries("Test Series", seriesToAdd2)).toBe(true);
    expect(data.allSeries.size).toBe(1);
    expect(data.allSeries.values().next().value).toEqual(seriesToAdd2);
  });
  it("will not replace a series that does not exist", () => {
    expect(data.replaceSeries("Not A Series", seriesToAdd)).toBe(false);
  });
  it("can check if a series exists", () => {
    data.addSeries(seriesToAdd);
    expect(data.doesSeriesExist("Test Series")).toBe(true);
    expect(data.doesSeriesExist("Not A Series")).toBe(false);
  });
});
