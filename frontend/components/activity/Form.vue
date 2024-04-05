<template>
    <form class="activity-input-form" @submit.prevent="$emit('submit', $event)">
        <div class="heading">
            <h2>{{ title }}</h2>
            <span class="description" v-text="descriptionValue"></span>
        </div>
        <CommonBanner v-bind="{ bannerType: BannerType.WARNING, bannerText }" />
        <div class="input-fields-grid">
            <fieldset class="input-group">
                <div class="control-groups">
                    <slot />
                </div>
            </fieldset>
        </div>
        <button type="submit" class="form-submit-button">
            {{ buttonTitle }}
        </button>
  </form>
</template>

<script setup lang="ts">
defineProps({
  title: {
    type: String,
    default: "Sign Up",
  },
  buttonTitle: {
    type: String,
    default: "Sign Up",
  },
  descriptionValue: {
    type: String,
    default: "",
  },
  bannerText: {
    type: String,
    default: "",
  },
});
defineEmits(["submit"]);
</script>

<style lange="scss" scoped>
.input-group {
  border: none;
}


</style>