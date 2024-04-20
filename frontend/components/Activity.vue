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
    padding: $large-text-size;

    h1 {
        color: $dark-orange-color;

        font-size: $large-title-size;
        font-weight: $header-text-weight;
        letter-spacing: .1ch;
    }
}
.activity-bar {
    width: 100%;
    justify-content: space-between;

    padding: $medium-large-text-size;
}

.activity-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    padding: $medium-large-text-size;

    color: $white-color;
    font-weight: $thin-text-weight;
}
</style>
