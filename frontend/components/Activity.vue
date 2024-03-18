<template>
    <div class="header-content">
        <h1>
            <slot name="header" />
        </h1>
    </div>
    <div class="activity-container">
        <div class="activity-bar">
            <slot name="bar" />
        </div>
        <slot name="content" />
    </div>
</template>

<style lang="scss" scoped>
.header-content {
    h1 {
        color: $dark-purple-color;
    }
}
</style>
