<template>
  <form class="pure-form-1-2 pure-form-aligned" @submit.prevent="handleLogin">
    <fieldset class="pure-group">
      <span>{{ userLoginError }}</span>
      <div class="pure-control-group">
        <label for="aligned-identifier">Username or Email</label>
        <input
            id="aligned-identifier"
            type="text"
            class="pure-input-1-2"
            placeholder="Username or Email"
            v-model="identifier"
        />
      </div>
      <div class="pure-control-group">
        <label for="aligned-password">Password</label>
        <input
            id="aligned-password"
            type="password"
            class="pure-input-1-2"
            placeholder="Password"
            v-model="password"
        />
      </div>
    </fieldset>
    <button
      type="submit"
      class="pure-button pure-input-1-2 pure-button-primary"
    >
      Sign in
    </button>
  </form>
</template>


<script setup lang="ts">
definePageMeta({
  layout: "landing",
});

const identifier = defineModel('identifier', {
  type: String,
  default: "",
});
const password = defineModel('password', {
  type: String,
  default: "",
});
const userLoginError = defineModel('userLoginError', {
      type: String,
      default: "",
    });

const handleLogin = async (): Promise<void> => {

    const userStore = getUserStore();
    await useBaseFetch("/login", {
      method: "POST",
      body: JSON.stringify({
        identifier: identifier.value,
        password: password.value,
      }),
    }).then(({data, error}) => {
        if (error) {
          const errorContent = error.value
          if(errorContent?.statusCode === 401) {
            userLoginError.value = "Invalid username or password"
          } else {
            userLoginError.value = "An error occurred"
            throw error;
          }
          return;
        }
        // const { user } = data.value;
        // userStore.login(user.username)
    })
    .catch((error) => {
      console.log(error);
      //throw error;
    });

};


</script>
