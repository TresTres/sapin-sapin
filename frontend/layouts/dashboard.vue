<template>
  <div class="dashboard-container">
    <Navbar :routes="appRoutes" />
    <div class="dashboard-content">
      <slot />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.dashboard-container {
  height: 100dvh;
  width: 100dvw;
  display: flex;
  align-items: stretch;
  flex-direction: row;

  background-image: radial-gradient(
    farthest-corner circle at 90% 90%,
    $primary-purple-color 0%,
    adjust-alpha($primary-purple-color, 50%) 20%,
    adjust-alpha($primary-purple-color, 10%) 50%,
    adjust-alpha($dark-purple-color, 100%) 90%
  );
  background-color: $dark-purple-color;
}

.dashboard-content {
  display: flex;
  height: 100%;
  width: 100%;
  align-items: stretch;
  flex-direction: column;
  padding: $medium-large-text-size;
}
</style>
