<template>
  <div class="control-group">
    <label v-if="label" for="aligned-identifier">{{ label }}</label>
    <input
      :id="`aligned-identifier-${index}`"
      class="user-input"
      :type="isPassword ? 'password' : 'text'"
      :placeholder="placeholder"
      v-model="inputValue"
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
  
  margin-bottom: 1rem;
  padding: 0.5rem;

  width: 100%;


  input {

    padding: 0.5rem;
    width: 90%;


    border: 1px solid #ccc;
    border-radius: 0.25rem;

  
    font-size: 1.3rem;

  }
}

label {
  display: none;
}



</style>