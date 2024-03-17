<template>
  <form class="user-input-form" @submit.prevent="$emit('submit', $event)">
    <div class="heading">
      <h1>{{ title }}</h1>
      <span class="description" v-text="descriptionValue"></span>
    </div>
    <span class="banner" v-text="bannerText"></span>
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
  },
  bannerText: {
    type: String,
    default: "",
  },
});

defineEmits(["submit"]);
</script>

<style lang="scss" scoped>
.user-input-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3vh;

  width: 100%;
  padding: 0.5rem;

  border: none;
}

.heading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1vh;

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

  padding: 0.2rem;
}

.input-group {
  border: none;

  .control-groups {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4vh;
  }
}

.form-submit-button {
  padding: 0.5rem 1.3rem;

  font-size: $large-text-size;

  background-color: $dark-purple-color;
  color: $white-color;
  opacity: 0.8;

  border: none;
  border-radius: 0.75rem;

  &:hover {
    background-color: $white-color;
    color: $dark-purple-color;
  }
}
</style>
