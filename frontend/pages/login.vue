import { UserResponseObject, UserObject } from '../stateless/interfaces/response-objects';
<template>

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
      router.push("/");
    })
    .catch((error) => {
      userLoginError.value = error.message;
    });
};
</script>
