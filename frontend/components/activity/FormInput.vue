<template>
    <div class="control-group">
      <label v-if="label" for="aligned-identifier">{{ label }}</label>
      <input
        :id="`${label}-${index}`"
        v-model="inputValue"
        class="input-field"
        :placeholder="placeholder"
        required
      />
    </div>
  </template>
  
  <script setup lang="ts">
  defineProps({
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

    background-color: adjust-alpha($white-color, 20%);
    color: $white-color;

    font-size: $medium-large-text-size;

    ::placeholder {
      color: $light-purple-color
    }
  }
  </style>
