
import type { UseFetchOptions } from "nuxt/app"
export const useBaseFetch: typeof useFetch = <T>(request: string, opts?: UseFetchOptions<T> ) => {
    /*
    Enforces the use of the backend base URL for requests.
    */


    const config = useRuntimeConfig()
    return useFetch(request, { baseURL: `${config.public.backendUrl}/v${config.public.apiVersion}`, ...opts })
}
