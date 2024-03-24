<template>
    <div class="banner-container" v-if="bannerText">
        <div class="banner-area">
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
</style>