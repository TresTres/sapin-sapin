<template>
  <div class="page-content">
    <div class="landing-card">
      <slot />
    </div>
  </div>
  <div class="footer">
    <div>Footer Text</div>
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

  background-image: radial-gradient(
    farthest-corner circle at 30% 40%,
    $light-purple-color 30%,
    $primary-purple-color
  );
  background-color: $light-purple-color;

  border-radius: 18px;

  box-shadow:
    2px 4px 8px 0 rgba(0, 0, 0, 0.2),
    4px 6px 20px 0 rgba(0, 0, 0, 0.19);

  overflow: hidden;
}

.footer {
  width: 100%;
  bottom: 0;
  padding: 2vh;

  text-align: center;
  font-size: 0.6rem;

  color: $gray-color;
}
</style>
