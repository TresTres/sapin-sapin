<template>
  <div class="form-container">
    <h1>{{ title }}</h1>
    <form class="user-input-form" @submit.prevent="$emit('submit', $event)">
      <fieldset class="input-group">
        <span v-text="bannerValue"></span>
        <slot />
      </fieldset>
      <button type="submit" class="form-submit-button">
        {{ buttonTitle }}
      </button>
    </form>
  </div>
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
  });

  const bannerValue = defineModel("bannerValue", {
  type: String,
  default: "",
});

  defineEmits(["submit"]);
</script>

<style lang="scss" scoped>
  .form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;

    h1 {
      
      font-size: $large-title-size;

      padding-bottom: 1rem;
    }
  }

  .user-input-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;

    border: none;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;

    border: none;
  }

  .form-submit-button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    font-size: $medium-text-size;
    background-color: $dark-purple-color;
    color: $light-color;

    border: solid $light-color 1px;


    &:hover {
      background-color: $light-color;
      color: $dark-purple-color;

      border: solid $dark-purple-color 1px;
    }
    
  }
</style>