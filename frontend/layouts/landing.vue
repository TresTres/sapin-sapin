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

    display: block;
    
    height: 90%;
    width: 80%;
    padding: .1vh 0;
    margin: 0 auto;

    background-color: $primary-green-color;

    border-style: solid;
    border-color: $dark-color;
    border-radius: 0 0 1% 1%;
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