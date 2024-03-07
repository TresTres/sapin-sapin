export type SimplifiedApiResponseObject = {
  status: number;
  headers: Record<string, string>;
  payload: Record<string, any> | null;
  error: Record<string, any> | null;
};