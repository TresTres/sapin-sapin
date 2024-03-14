<template>
  <div class="dashboard-container">
    <slot name="header" />
    <slot />
  </div>
</template>

<style lang="scss">

.dashboard-container {
  display: flex;
  flex-direction: row;
}
</style>
