<template>
  <div class="landing-container">
    <div class="image-area">
      <NuxtImg preload src="/draft_theme.jpeg" sizes="40vw" loading="lazy" />
    </div>
    <div class="form-area">
      <UserForm
        :banner-text="authStore.authError"
        title="Login"
        button-title="Sign In"
        description-value="Please enter your credentials to sign in."
        @submit="handleLogin"
      >
        <UserFormInput
          v-model:inputValue="identifier"
          :label="identifierLabel"
          :index="0"
          :is-password="false"
          :placeholder="identifierLabel"
        />
        <UserFormInput
          v-model:inputValue="password"
          :label="passwordLabel"
          :index="1"
          :is-password="true"
          :placeholder="passwordLabel"
        />
      </UserForm>
      <!-- <UserRegistration /> -->
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  title: "Login",
  layout: "landing",
});

const identifierLabel = "Username or Email";
const passwordLabel = "Password";
const identifier = ref("");
const password = ref("");

const authStore = useAuthStore();

const handleLogin = async (): Promise<void> => {
  await authStore.login(identifier.value, password.value);
};
</script>

<style lang="scss" scoped>
.landing-container {
  position: relative;
  display: flex;
  flex-direction: row;

  align-content: space-around;
}

.image-area {
  max-width: 70%;
  height: 100%;

  border-right: 2px $black-color solid;

  overflow: hidden;
  img {
    height: 110%;

    object-fit: cover;
  }
}

.form-area {
  width: 50%;
  height: 100%;

  display: flex;
  flex-direction: column;
  align-items: center;

  padding: 2rem;
}
</style>
