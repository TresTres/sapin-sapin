import type { UseFetchOptions } from '#app';
import { FetchError } from 'ofetch';


export const useAuthorizingFetch = async (request: string, opts?: UseFetchOptions<any> ) => {
  /*
  * This function is a wrapper around useFetch that will attempt to contact protected routes.
  * These routes require a valid access token present in the request headers.  
  * If we don't have an acces token in memory, or if it's expired, we will attempt to get a new one, and then retry the request.
  */

  const authStore = useAuthStore();
  try {
    if (!authStore.accessToken) {
      throw Error("No token found");
    }
    // try inital request
    return await useFetch(request, {
      ...opts, headers: { Authorization: `Bearer ${authStore.accessToken}` } 
    });
  } catch (error: any) {
    if(error.status === 401 || error.message == "No token found") {
      // attempt to get a new token
      await authStore.refreshToken();
      if (authStore.accessToken) {
        // try request again
        return await useFetch(request, {
          ...opts, headers: { Authorization: `Bearer ${authStore.accessToken}` } 
        }).catch((error: FetchError): FetchError => {
          console.error(error.data);
          return error;
        });
      }
    } 
    if(error instanceof FetchError) {
      console.error(error.data);
    } else {
      console.error(error);
    }
    return error;
  }
};
