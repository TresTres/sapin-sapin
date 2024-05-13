<template>
  <div class="control-group">
    <label v-if="label" for="aligned-identifier">{{ label }}</label>
    <input
      :id="`aligned-identifier-${index}`"
      v-model="inputValue"
      class="user-input"
      :type="isPassword ? 'password' : 'text'"
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

<style lang="scss" scoped>
.control-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.user-input {
  padding: 0.5rem 2rem;
  width: 100%;

  border: none;
  border-radius: 0.7em;

  background-color: color.adjust($white-color, $alpha: -0.5);
  color: $dark-purple-color;

  font-size: $medium-large-text-size;
}

.user-input::placeholder {
  color: color.adjust($dark-purple-color, $alpha: -0.4);
}

.user-input:focus {
  outline: 2px solid $light-purple-color;
  color: $primary-purple-color;
}

label {
  @include label;
}
</style>
