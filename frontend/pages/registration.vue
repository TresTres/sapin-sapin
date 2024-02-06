<template>
  <UserForm
    :controlGroups="registrationFields"
    :submitButtonText="'Register'"
    :handleSubmit="handleRegistration"
    :errorTextModel="userRegistrationError"
  />
</template>

<script setup lang="ts">
definePageMeta({
  layout: "landing",
});

const username = defineModel("username", {
  type: String,
  default: "",
});
const email = defineModel("email", {
  type: String,
  default: "",
});
const password = defineModel("password", {
  type: String,
  default: "",
});
const userRegistrationError = defineModel("userRegistrationError", {
  type: String,
  default: "",
});

const registrationFields = [
  {
    label: "Username",
    placeholder: "Username",
    value: username.value,
  },
  {
    label: "Email",
    placeholder: "Email",
    value: email.value,
  },
  {
    label: "Password",
    placeholder: "Password",
    value: password.value,
    isPassword: true,
  },
];

const handleRegistration = async (): Promise<void> => {
  console.log(username.value, email.value, password.value)
  await useBaseFetch("/registration", {
    method: "POST",
    body: JSON.stringify({
      username: username.value,
      email: email.value,
      password: password.value,
    }),
  }).then(({ data, error }) => {
    if (error) {
      const errorContent = error.value;
      if (errorContent?.statusCode === 409 || errorContent?.statusCode === 400) {
        userRegistrationError.value = errorContent.data.message;
      } else {
        userRegistrationError.value = "An error occurred";
      }
    }
  });
};
</script>
