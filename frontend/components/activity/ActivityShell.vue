<template>
  <div class="header-content">
    <h1>
      <slot name="header" />
    </h1>
  </div>
  <div class="activity-container">
    <!-- <div class="activity-bar">
            <slot name="bar" />
        </div> -->
    <slot name="content" />
  </div>
</template>

<style lang="scss">
.header-content {
  flex: 1;
  padding: $small-text-size;

  h1 {
    color: $primary-orange-color;

    font-size: $large-title-size;
    font-weight: $header-text-weight;
    letter-spacing: 0.1ch;
    p {
      color: $primary-orange-color;

      font-size: $standard-text-size;
      font-weight: $standard-text-weight;
    }
  }
}
// .activity-bar {
//     width: 100%;
//     justify-content: space-between;

//     padding: $medium-large-text-size;
// }

.activity-container {
  flex: 12;
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  padding: $standard-text-size;

  color: $white-color;
  font-weight: $thin-text-weight;
}
</style>
