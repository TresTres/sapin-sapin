<template>
  <div class="control-group">
    <label v-if="label" for="aligned-identifier">{{ label }}</label>
    <textarea
      v-if="inputType == InputType.AREA"
      :id="`${label}-${index}`"
      v-model="inputValue"
      class="input-field input-area"
      rows="5"
      :placeholder="placeholder"
      required
    />
    <input
      v-else
      :id="`${label}-${index}`"
      v-model="inputValue"
      class="input-field"
      :placeholder="placeholder"
      :type="inputType"
      required
    />
  </div>
</template>

<script setup lang="ts">
  defineProps({
    inputType: {
      type: InputType,
      default: InputType.TEXT,
    },
    label: {
      type: [String, Boolean],
      default: false,
    },
    index: {
      type: [Number],
      default: 0,
    },
    placeholder: {
      type: String,
      required: true,
    },
  });

  const inputValue = defineModel("inputValue", {
    type: String,
    default: "",
  });
</script>

<style lang="scss" scoped>
  .control-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }

  .input-field {
    padding: 0.5rem 2rem;
    width: 100%;

    border: none;
    border-radius: 0.7em;

    background-color: adjust-alpha($white-color, 50%);
    color: $dark-purple-color;

    font-size: $medium-large-text-size;

    &::placeholder {
      color: adjust-alpha($dark-purple-color, 50%);
    }

    &:focus {
      outline: 2px solid $primary-purple-color;
      color: $primary-purple-color;
    }
  }

  .input-area {
    resize: none;
    overflow: auto;
  }
</style>
