import type { DataEventSeries } from './state-objects';

export type UserResponseObject = {
  username: string;
  email: string;
  date_joined: string;
};


export type DataEventSeriesResponseObject = {
  owned_series: DataEventSeries[];
};