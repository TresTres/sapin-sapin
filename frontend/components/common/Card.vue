<template>
  <div class="card">
    <slot />
  </div>
</template>

<style lang="scss">
  .card {
    padding: $medium-large-text-size;
    background-color: adjust-alpha($light-purple-color, 15%);
    @include small-box-shadow();
    border-radius: 1.3rem;

    overflow: auto;
  }
</style>