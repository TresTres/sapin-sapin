export const useBaseFetch: typeof useFetch = (request, opts?) => {
  /*
    Enforces the use of the backend base URL for requests.
    */

  const config = useRuntimeConfig();
  const authStore = getAuthStore();
  return useFetch(request, {
      baseURL: `${config.public.backendUrl}/v${config.public.apiVersion}`,
      ...opts,
      onRequest: ({ options }) => {
          options.headers = {
              ...options.headers,
              Authorization: authStore.bearerToken,
          };
      }
    },
  );
};
