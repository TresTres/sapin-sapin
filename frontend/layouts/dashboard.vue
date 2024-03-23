<template>
  <div class="dashboard-container">
    <slot name="header" />
    <div class="dashboard-content">
      <slot />
    </div>
  </div>
</template>

<style lang="scss">

.dashboard-container {
  display: flex;
  flex-direction: row;
}

.dashboard-content {
  
  padding: 3rem;
}
</style>
