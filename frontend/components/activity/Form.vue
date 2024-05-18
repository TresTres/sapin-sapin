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
    display: flex;

    flex-direction: column;
    align-items: stretch;

    height: 100%;
    box-sizing: border-box;
  }

  .heading {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;
  }

  .input-fields {

    flex: 12;

    width: 100%;
    box-sizing: border-box;

    border: none;
    overflow: auto;
  }

  .button-field {
    flex: 1;
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .form-submit-button {
    @include large-button;

    max-width: 35%;
  }
</style>
