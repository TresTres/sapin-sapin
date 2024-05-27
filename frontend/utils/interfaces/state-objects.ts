export type DataEvent = {
  label: string;
  description: string;
  date: Date;
  amount: number;
};

export type DataRecurrence = {
  label: string;
  description: string;
  startDate: Date;
  endDate?: Date;
  interval: number;
  amount: number;
};

export type DataEventSeries = {
  id: string;
  title: string;
  description: string;
  events: DataEvent[];
  recurrences: DataRecurrence[];
};
