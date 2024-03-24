<template>
    <div class="banner-container" v-if="bannerText">
        <div class="banner-area" :class="bannerType.toLowerCase()">
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
    padding: 1rem;
    border-radius: 0.5rem;
    border: 3px solid;

    h1 {
        font-size: $medium-text-size;
    }
    p {
        font-size: $standard-text-size;
    }
}





</style>