export const useBaseFetch: typeof useFetch = (request, opts?) => {
  /*
    Enforces the use of the backend base URL for requests.
    */

  const config = useRuntimeConfig();
  return useFetch(request, {
      baseURL: `${config.public.backendUrl}/v${config.public.apiVersion}`,
      ...opts,
    },
  );
};

export const useAuthenticatingFetch: typeof useFetch = (request, opts?) => {
  /*
  Include the bearer token in the request headers.
  */

  const pinia = useNuxtApp().$pinia;
  const authStore = getAuthStore(pinia);
  console.log(authStore.bearerToken)
  return useBaseFetch(request, {
      ...opts,
      headers: {
        ...opts?.headers,
        Authorization: `${authStore.bearerToken}`,
      },
    },
  );
}