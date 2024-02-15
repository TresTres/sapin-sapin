<template>
    <div class="header">
        <slot name="header"/>
    </div>
    <div class="pure-g">
        <slot />
    </div>
    <div class="footer">
        <slot name="footer"/>
    </div>
</template>


<style lang="scss" scoped>
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  color: $dark-color;
  text-align: center;
  padding: 2vh;
}
</style>