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

<style lang="scss" scoped>
  .input-group {
    border: none;
  }

  .heading {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;

 }

 .form-submit-button {
   padding: 0.5rem 1rem;
   border: none;
   border-radius: 0.7em;
   background-color: $primary-purple-color;
   color: $white-color;
   font-size: $medium-large-text-size;
   cursor: pointer;
   transition: background-color 0.3s;
 }
</style>
