import { FetchError, type FetchResponse, type FetchOptions } from "ofetch";
import { useAuthStore } from "../stores/auth";

type FetchRequestMethod =
  | "GET"
  | "HEAD"
  | "PATCH"
  | "POST"
  | "PUT"
  | "DELETE"
  | "CONNECT"
  | "OPTIONS"
  | "TRACE"
  | "get"
  | "head"
  | "patch"
  | "post"
  | "put"
  | "delete"
  | "connect"
  | "options"
  | "trace"
  | undefined;

export const useAuthorizingFetch = async (
  request: string,
  opts?: FetchOptions<any>,
): Promise<any> => {
  /*
   * This function is a wrapper around useFetch that will attempt to contact protected routes.
   * These routes require a valid access token present in the request headers.
   * If we don't have an acces token in memory, or if it's expired, we will attempt to get a new one, and then retry the request.
   */

  const authStore = useAuthStore();
  try {
    if (!authStore.accessToken) {
      throw new Error("No token found");
    }
    // try inital request
    return await $fetch(request, {
      ...opts,
      method: (opts?.method as FetchRequestMethod) || "GET",
      headers: { Authorization: `Bearer ${authStore.accessToken}` },
    });
  } catch (error: any) {
    if (error.status === 401 || error.message == "No token found") {
      // attempt to get a new token
      await refreshAccessToken();
      if (authStore.accessToken) {
        // try request again
        return await $fetch(request, {
          ...opts,
          method: (opts?.method as FetchRequestMethod) || "GET",
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        });
      }
    }
    throw error;
  }
};

const refreshAccessToken = async (): Promise<void> => {
  /*
   * This function will attempt to get a new access token using the refresh token.
   * If successful, it will update the authStore with the new access token.
   */

  const authStore = useAuthStore();
  let refreshToken = useCookie("refresh_token").value;
  if (process.server) {
    const app = useNuxtApp();
    const contextNode = app.ssrContext?.event.node;
    const requestCookies = contextNode?.req.headers.cookie;
    refreshToken =
      requestCookies
        ?.split(";")
        .find((c: string) => c.includes("refresh_token"))
        ?.split("=")[1] || "";
  }
  await $fetch
    .raw("/api/me/refresh", {
      method: "GET",
      headers: { Cookie: `refresh_token=${refreshToken}` },
    })
    .then(async (resp: FetchResponse<any>): Promise<void> => {
      const {
        headers,
        _data: { user },
      } = resp;
      authStore.authError = "";
      authStore.accessToken = headers.get("Authorization")?.split(" ")[1] || "";
    })
    .catch((error: FetchError): void => {
      console.error(error);
      authStore.clearAuth();
      if (error.status === 401) {
        authStore.authError = "Invalid refresh token.";
      } else {
        authStore.authError =
          "An error occurred on refresh.  Please retry login.";
      }
    });
};
