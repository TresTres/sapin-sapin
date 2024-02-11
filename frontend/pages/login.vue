<template>
  <form class="pure-form-1-2 pure-form-aligned" @submit.prevent="handleLogin">
    <fieldset class="pure-group">
      <span v-text="authError"></span>
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
</template>

<script setup lang="ts">
definePageMeta({
  layout: "landing",
});

const identifierLabel = "Username or Email";
const passwordLabel = "Password";
const identifier = ref("");
const password = ref("");

const authStore = getAuthStore();
const { authError } = storeToRefs(authStore);

const handleLogin = async (): Promise<void> => {
  await authStore.login(identifier.value, password.value);
};
</script>
