export default defineEventHandler(async (event): Promise<any> => {
  const config = useRuntimeConfig(); // implemented in Nitro, not just a composable
  const proxyUrl = `${config.public.backendUrl}/v${config.public.apiVersion}`;
  const proxyTarget = event.path.replace(/^\/api/, proxyUrl);

  return proxyRequest(event, proxyTarget); // proxyRequest originates from h3
});