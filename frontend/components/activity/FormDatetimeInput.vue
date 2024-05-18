<!-- component that handles datetime -->

<template>
  <div class="control-group">
    <label v-if="label" for="aligned-identifier">
      {{ label }}
      <span v-if="required" class="required">*required</span>
    </label>
    <div class="formatted-date">
      <input
        type="datetime-local"
        :id="`${label}-${index}-date`"
        class="date-field"
        :placeholder="placeholder"
        :required="required"
        v-model="dateValue"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
  interface Props {
    label: string | boolean;
    index?: number;
    placeholder: string;
    required?: boolean;
  }

  withDefaults(defineProps<Props>(), {
    label: false,
    index: 0,
    required: false,
  });

  const dateValue = defineModel<Date>("dateValue", {
    required: true,
    default: new Date(),
  });

</script>

<style lang="scss" scoped>

  .control-group {
    display: flex;
    flex-direction: column;
  }

  label {
    @include input-label;
  }

  .required {
    @include required-label;
  }

  .formatted-date {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;

  }
  .date-field {
    @include text-input;
  }

</style>