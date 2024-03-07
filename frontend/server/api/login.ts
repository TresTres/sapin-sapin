import { backendFetch } from "../utils/fetch";
import { FetchError, FetchResponse } from "ofetch";

export default defineEventHandler(async (event): Promise<SimplifiedApiResponseObject> => {
  return await backendFetch<FetchResponse<any> | FetchError<any>>(
    "login", {
      method: "POST",
      body: await readBody(event),
    }
  ).then((response: FetchResponse<any>) => {  
    return {
      status: response.status,
      headers: response.headers,
      payload: response._data,
      error: null,
    }
  }).catch((error: FetchError<any>) => {
    return {
      status: error.status,
      headers: error.data.headers || {},
      payload: null,
      error: error.data,
    }
  });
});