<template>
  <div class="landing-container">
    <div class="image-area">
      <NuxtImg src="/draft_theme.jpeg" sizes="40vw" placeholder />
    </div>
    <div class="form-area">
      <h1>Login</h1>
      <UserLogin />
    <!-- <UserRegistration /> -->
    </div>
  </div>


</template>

<script setup lang="ts">
    definePageMeta({
        title: "Home Page",
        layout: "landing"
    })


const userStore = getUserStore();
</script>

<style lang="scss" scoped>
.landing-container {
  position: relative;
  display: flex;
  flex-direction: row;
  
  align-content: space-around;
}

.image-area {
  width: 45%;
  height: 100%;

  border-right: 2px $dark-color solid;

  overflow: hidden;

  img {
    height: 100%;

    object-fit: cover;
  }

}

</style>
