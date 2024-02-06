<template>
  <form
    class="pure-form-1-2 pure-form-aligned"
    @submit.prevent="handleRegistration"
  >
    <fieldset class="pure-group">
      <span v-text="userRegistrationError"></span>
      <div>
        <UserFormInput
          :label="usernameLabel"
          :index="0"
          :isPassword="false"
          :placeholder="usernameLabel"
          v-model:inputValue="username"
        />
        <UserFormInput
          :label="emailLabel"
          :index="1"
          :isPassword="false"
          :placeholder="emailLabel"
          v-model:inputValue="email"
        />
        <UserFormInput
          :label="passwordLabel"
          :index="2"
          :isPassword="true"
          :placeholder="passwordLabel"
          v-model:inputValue="password"
        />
        <UserFormInput
          :label="confirmPasswordLabel"
          :index="3"
          :isPassword="true"
          :placeholder="confirmPasswordLabel"
          v-model:inputValue="confirmPassword"
        />
      </div>
    </fieldset>
    <button
      type="submit"
      class="pure-button pure-input-1-2 pure-button-primary"
    >
      Sign Up
    </button>
  </form>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "landing",
});

const userRegistrationError = defineModel("userRegistrationError", {
  type: String,
  default: "",
});
const usernameLabel = "Username";
const emailLabel = "Email";
const passwordLabel = "Password";
const confirmPasswordLabel = "Confirm Password";
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

const validatePasswordMatch = async (): Promise<boolean> => {
  return new Promise<boolean>((resolve) =>
    resolve(confirmPassword.value === password.value)
  );
};

const handleRegistration = async (): Promise<void> => {
  await validatePasswordMatch()
    .then((doesMatch) => {
      if (!doesMatch) {
        throw new Error("Passwords do not match");
      }
    })
    .then(() =>
      useBaseFetch("/registration", {
        method: "POST",
        body: JSON.stringify({
          username: username.value,
          email: email.value,
          password: password.value,
        }),
      })
    )
    .then(({ data, error }) => {
      const errorContent = error.value;
      if (errorContent) {
        if (
          errorContent?.statusCode === 409 ||
          errorContent?.statusCode === 400
        ) {
          throw new Error(errorContent.data.message);
        } else {
          throw new Error("Unspecified error");
        }
      }
      userRegistrationError.value = "Registration successful";
    })
    .catch((error) => {
      userRegistrationError.value = error.message;
    });
};
</script>
