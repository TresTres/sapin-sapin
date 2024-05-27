<template>
  <form
    class="pure-form-1-2 pure-form-aligned"
    @submit.prevent="handleRegistration"
  >
    <fieldset class="pure-group">
      <span v-text="userRegistrationError"></span>
      <div>
        <UserFormInput
          v-model:inputValue="username"
          :label="usernameLabel"
          :index="0"
          :is-password="false"
          :placeholder="usernameLabel"
        />
        <UserFormInput
          v-model:inputValue="email"
          :label="emailLabel"
          :index="1"
          :is-password="false"
          :placeholder="emailLabel"
        />
        <UserFormInput
          v-model:inputValue="password"
          :label="passwordLabel"
          :index="2"
          :is-password="true"
          :placeholder="passwordLabel"
        />
        <UserFormInput
          v-model:inputValue="confirmPassword"
          :label="confirmPasswordLabel"
          :index="3"
          :is-password="true"
          :placeholder="confirmPasswordLabel"
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

const validatePasswordMatch = (): Promise<boolean> => {
  return new Promise<boolean>((resolve) =>
    resolve(confirmPassword.value === password.value),
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
      useFetch("/registration", {
        method: "POST",
        body: JSON.stringify({
          username: username.value,
          email: email.value,
          password: password.value,
        }),
      }),
    )
    .then(({ data, error }) => {
      const errorContent = error.value;
      if (errorContent || !data.value) {
        if (
          errorContent?.statusCode === 409 ||
          errorContent?.statusCode === 400
        ) {
          throw new Error(errorContent.data.message);
        } else {
          throw new Error("Unspecified error");
        }
      }
      const { newUser } = data.value;
      userRegistrationError.value = `Registration successful for username: ${newUser}.  Proceed to login.`;
    })
    .catch((error) => {
      userRegistrationError.value = error.message;
    });
};
</script>
