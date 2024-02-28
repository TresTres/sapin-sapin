<template>
  <div v-if="!userStore.isLoggedIn" class="landing-container">
    <div class="image-area">
      <NuxtImg preload src="/draft_theme.jpeg" sizes="40vw" loading="lazy" />
    </div>
    <div class="form-area">
      <UserForm
        title="Login"
        buttonTitle="Sign In"
        description-value="Please enter your credentials to sign in."
        v-model:bannerValue="userLoginError"
        @submit="handleLogin"
      >
        <UserFormInput
          :label="identifierLabel"
          :index="0"
          :isPassword="false"
          :placeholder="identifierLabel"
          v-model:inputValue="identifier"
        />
        <UserFormInput
          :label="passwordLabel"
          :index="1"
          :isPassword="true"
          :placeholder="passwordLabel"
          v-model:inputValue="password"
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

  const userLoginError = defineModel("userLoginError", {
    type: String,
    default: "",
  });
  const identifierLabel = "Username or Email";
  const passwordLabel = "Password";
  const identifier = ref("");
  const password = ref("");

  const userStore = getUserStore();
  const router = useRouter();

  const handleLogin = async (): Promise<void> => {
    await useBaseFetch("/login", {
      method: "POST",
      body: JSON.stringify({
        identifier: identifier.value,
        password: password.value,
      }),
    })
      .then(({ data, error }) => {
        const errorContent = error.value;
        if (errorContent) {
          if (errorContent?.statusCode === 401) {
            throw new Error("Invalid username or password");
          } else {
            throw new Error("An error occurred");
          }
        }
        const { user } = data?.value as { user: UserResponseObject };
        userLoginError.value = "Login successful";
        userStore.login(user);
        navigateTo("/");
      })
      .catch((error) => {
        userLoginError.value = error.message;
      });
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

    border-right: 2px $dark-color solid;

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
