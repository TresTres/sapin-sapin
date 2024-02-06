import { UserResponseObject, UserObject } from '../stateless/interfaces/response-objects';
<template>
  <form class="pure-form-1-2 pure-form-aligned" @submit.prevent="handleLogin">
    <fieldset class="pure-group">
      <span v-text="userLoginError"></span>
      <div>
        <UserFormInput
          :label="identifierLabel"
          :index=0
          :isPassword=false
          :placeholder="identifierLabel"
          v-model:inputValue="identifier"
        />
        <UserFormInput
          :label="passwordLabel"
          :index=1
          :isPassword=true
          :placeholder="passwordLabel"
          v-model:inputValue="password"
        />
      </div>
    </fieldset>
    <button
      type="submit"
      class="pure-button pure-input-1-2 pure-button-primary"
    >
      Login
    </button>
  </form>
</template>

<script setup lang="ts">
definePageMeta({
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
      const { user } = data?.value as UserResponseObject;
      userLoginError.value = "Login successful";
      userStore.login(user.username);
    })
    .catch((error) => {
      userLoginError.value = error.message;
    });
};
</script>
