<template>
  <form class="user-input-form" @submit.prevent="$emit('submit', $event)">
    <div class="heading"> 
      <h1>{{ title }}</h1>
      <span class="description" v-text="descriptionValue"></span>
    </div>
    <span class="banner" v-text="bannerValue"></span>
    <fieldset class="input-group">
      <div class="control-groups">
        <slot />
      </div>
    </fieldset>
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
    }
  });

  const bannerValue = defineModel("bannerValue", {
    type: String,
    default: "",
  });

  defineEmits(["submit"]);
</script>

<style lang="scss" scoped>
  .user-input-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3rem;

    width: 100%;
    padding: 1rem;

    border: none;

   
  }

  .heading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    

    h1 {
      font-size: $large-title-size;
      color: $dark-purple-color;

      text-transform: uppercase;
    }

    .description {

      font-size: $small-text-size;
      color: $dark-purple-color;
    }
  }


  .banner {
    font-size: $medium-text-size;
    color: $danger-color;

    padding: .2rem;
  }

    .input-group {
      border: none;

      .control-groups {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3rem;
      }
    }

  .form-submit-button {

    padding: .5rem 1.3rem;

    font-size: $large-text-size;

    background-color: $dark-purple-color;
    color: $light-color;
    opacity: .8;

    border: none;
    border-radius: .75rem; 

    &:hover {
      background-color: $light-color;
      color: $dark-purple-color;
    }
  }
</style>
