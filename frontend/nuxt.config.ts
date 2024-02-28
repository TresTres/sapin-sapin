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
    "@nuxt/image",
  ],
  imports: {
    dirs: ["stateless/**/*"],
  },
  css: ["@/assets/scss/main.scss"],
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
                          @use 'sass:color';
                          @import "@/assets/scss/_theme.scss";
                          @import "@/assets/scss/_font.scss";
                          `,
        },
      },
    },
  },
});
