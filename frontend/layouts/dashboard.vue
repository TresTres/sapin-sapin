<template>
  <div class="dashboard-container">
    <slot name="header" />
    <p>other</p>
    <slot />
  </div>
</template>

<style lang="scss">

.dashboard-container {
  display: flex;
  flex-direction: row;
}
</style>
