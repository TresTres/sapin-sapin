<template>
  <Activity> 
    <template #header> 
      Profile 
    </template>
    <template #content>
      <ClientOnly>
        <CommonCard class="profile-card">
          <p>Username: {{ username }}</p>
          <p>Email: {{ email }}</p>
          <p>Account age: {{ accountAge.toFixed(2) }} days</p>
          <button
            class="logout-button"
            @click="logout"
          >
            Logout
          </button>
        </CommonCard>
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

<style lang="scss" scoped>
.profile-card {
  display: block;
  width: 40%;
  padding: $medium-large-text-size;

  font-size: $medium-large-text-size;
}

.logout-button {

  padding: $small-text-size $medium-large-text-size;
  margin: $medium-large-text-size;

  font-size: $large-text-size;
  
  background-color: $dark-orange-color;
  color: $white-color;
  opacity: 0.8;

  border: none;
  border-radius: 0.75rem;


  &:hover {
    background-color: $white-color;
    color: $primary-orange-color;
  }

}
</style>
