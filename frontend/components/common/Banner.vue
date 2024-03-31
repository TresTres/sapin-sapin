<template>
    <div class="banner-container" v-if="bannerText">
        <div class="banner-area" :class="`notify-${bannerType.toLowerCase()}`">
            <h1 class="logo-font">{{ bannerType }}</h1>
            <p>{{ bannerText }}</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { BannerType } from '@/utils/constants';

defineProps<{
    bannerType: BannerType;
    bannerText: string;
}>();

</script>

<style lang="scss" scoped>

.banner-container {
    display: flex;
    justify-content: center;
    width: 70%;
    max-height: 20%;

}

.banner-area {
    /* 
    The banner area also adopts the theme colors toggled on the bannerType prop, 
    e.g., notify-warning
    See the notify-* classes in assets/scss/_theme.scss.
    */
    padding: $small-text-size;
    border-radius: 0.5rem;
    @include small-box-shadow();

    h1 {
        font-size: $standard-text-size;
    }
    p {
        font-size: $small-text-size;
    }
}


</style>