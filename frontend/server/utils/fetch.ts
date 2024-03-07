export const backendFetch = <T>(resource: string, opts?: any) : Promise<any> => {
  /*
    Enforces the use of the backend base URL for requests.
  */

  const config = useRuntimeConfig();

  return $fetch.raw<T>(
    `${config.public.backendUrl}/v${config.public.apiVersion}/${resource}`,
    {
      ...opts,
    }
  );
};
