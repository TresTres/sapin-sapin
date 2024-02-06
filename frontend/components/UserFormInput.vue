<template>
  <div class="pure-control-group">
    <label v-if="label" for="aligned-identifier">{{ label }}</label>
    <input
      :id="`aligned-identifier-${index}`"
      class="pure-input-1-2"
      :type="isPassword ? 'password' : 'text'"
      :placeholder="placeholder"
      v-model="inputValue"
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
  isPassword: {
    type: Boolean,
    default: false,
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
