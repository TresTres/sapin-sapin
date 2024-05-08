<template>
  <form class="activity-input-form" @submit.prevent="$emit('submit', $event)">
    <div class="heading">
      <h2>{{ title }}</h2>
      <span class="description" v-text="descriptionValue"></span>
    </div>
    <CommonBanner v-bind="{ bannerType: BannerType.WARNING, bannerText }" />
    <fieldset class="input-fields">
      <slot />
    </fieldset>
    <div class="button-field"> 
      <button type="submit" class="form-submit-button">
      {{ buttonTitle }}
      </button>
      <slot name="buttons" />
    </div>
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
  .activity-input-form {
    position: relative;
    display: flex;
    flex-direction: column;

    height: 100%;
  }

  .heading {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;
  }

  .input-fields {

    border: none;
    width: 100%;
    height: 100%;

    overflow: auto;
  }

  .button-field {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .form-submit-button {
    @include large-button;

    width: 20%;
  }
</style>
