<!-- component that handles various text inputs, e.g. text, textarea, and password -->

<template>
  <div class="control-group">
    <label v-if="label" for="aligned-identifier">
      {{ label }}
      <span v-if="required" class="required">*required</span>
    </label>
    <textarea
      v-if="inputType == FormInputType.AREA"
      :id="`${label}-${index}`"
      class="input-field input-area"
      rows="5"
      :placeholder="placeholder"
      :required="required"
      v-model="inputValue"
    />
    <input
      v-else
      :id="`${label}-${index}`"
      class="input-field"
      :placeholder="placeholder"
      :type="inputType"
      :required="required"
      v-model="inputValue"
    />
  </div>
</template>

<script setup lang="ts">
  interface Props {
    //it's nonsensical that TS complains about this for enums
    //@ts-expect-error: TS2749
    inputType?: FormInputType;
    label: string | boolean;
    index?: number;
    placeholder: string;
    required?: boolean;
  }

  withDefaults(defineProps<Props>(), {
    inputType: FormInputType.TEXT,
    label: false,
    index: 0,
    required: false,
  });

  const inputValue = defineModel<string>("inputValue", {
    required: true,
    default: "",
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

  .input-field {
    @include text-input;
  }

  .input-area {
    resize: none;
    overflow: auto;

    font-size: $standard-text-size;
    height: 6rem;
  }
</style>
