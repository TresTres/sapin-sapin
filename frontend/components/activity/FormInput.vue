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
  
