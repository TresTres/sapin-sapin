// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },


  runtimeConfig: {
    public: {
      backendUrl: process.env.BASE_URL || 'http://localhost:8000'
    }
  }
})
