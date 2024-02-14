// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      backendUrl: process.env.BASE_URL || "http://127.0.0.1:8000",
      apiVersion: process.env.API_VERSION || "DEV",
    },
  },

  modules: [
    [
      "@pinia/nuxt",
      {
        autoImports: ["defineStore"],
      },
    ],
  ],
  imports: {
    dirs: [
      'stateless/**/*'
    ]
  }
});
