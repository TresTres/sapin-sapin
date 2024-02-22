<template>
  <div class="landing-card-container">
    <div class="login-activity">
      <form class="card-form" @submit.prevent="handleLogin">
        <fieldset class="field-group">
          <span v-text="userLoginError"></span>
          <div>
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
          </div>
        </fieldset>
        <button
          type="submit"
          class="pure-button pure-input-1-2 pure-button-primary"
        >
          Login
        </button>
      </form>
    </div>
    <div class="registration-activity">
      <form class="card-form" @submit.prevent="handleRegistration">
        <fieldset class="field-group">
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
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "landing",
});

const userLoginError = defineModel("userLoginError", {
  type: String,
  default: "",
});
const userRegistrationError = defineModel("userRegistrationError", {
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
