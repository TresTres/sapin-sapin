export type DataEventSeries = {
  id: string;
  title: string;
  description: string;
  events: DataEvent[];
  recurrences: DataRecurrence[];
}

export type DataEvent = {
  label: string;
  description: string;
  date: Date;
  amount: number;
}

export type DataRecurrence = {
  label: string;
  description: string;
  start_date: Date;
  end_date?: Date;
  interval: number;
  amount: number;
}