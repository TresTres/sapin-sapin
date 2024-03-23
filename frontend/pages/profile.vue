<template>
  <Activity> 
    <template #header> 
      Profile 
    </template>
    <template #content>
      <ClientOnly>
        <div>
          <p>Username: {{ username }}</p>
          <p>Email: {{ email }}</p>
          <p>Account age: {{ accountAge.toFixed(2) }} days</p>
          <button
            class="pure-button pure-input-1-2 pure-button-primary"
            @click="logout"
          >
            Logout
          </button>
        </div>
      </ClientOnly>
    </template>
</Activity>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "dashboard",
});
const userStore = useUserStore();
const authStore = useAuthStore();
const { username , email,  accountAge } = storeToRefs(userStore);

const logout = async(): Promise<void> => {
  /*
    Logout the user and return to the login page
  */
  authStore.clearAuth();
  await navigateTo("/login");
};
</script>
