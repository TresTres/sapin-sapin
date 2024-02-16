<template>
    <div class="header">
        <slot name="header"/>
    </div>
    <div class="page-content">
        <slot />
    </div>
    <div class="footer">
        <slot name="footer"/>
    </div>
</template>


<style lang="scss" scoped>
.page-content {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  color: $dark-color;
  text-align: center;
  padding: 2vh;
}
</style>