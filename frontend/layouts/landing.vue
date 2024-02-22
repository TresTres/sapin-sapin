<template>
  <div class="page-content">
    <div class="landing-card">
      <slot />
    </div>
  </div>
  <div class="footer">
    <slot name="footer" />
  </div>
</template>

<style lang="scss" scoped>
.page-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.landing-card {
  height: 60vh;
  width: 60vw;

  background-image: radial-gradient(farthest-corner circle at 30% 40%,  $light-purple-color 10%, $primary-purple-color);
  background-color: $light-purple-color;


  border-style: solid;
  border-radius: 18px;
  border-width: 2px;
  border-color: $dark-purple-color;

}

.footer {
  width: 100%;
  bottom: 0;
  padding: 2vh;

  text-align: center;
  font-size: 0.5rem;

  color: $gray-color;
}
</style>
