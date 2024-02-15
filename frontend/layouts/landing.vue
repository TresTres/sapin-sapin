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
