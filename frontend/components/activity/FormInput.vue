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
      @input="
        $emit('update:inputValue', ($event.target as HTMLInputElement)?.value)
      "
      :placeholder="placeholder"
      :required="required"
    />
    <input
      v-else
      :id="`${label}-${index}`"
      class="input-field"
      @input="
        $emit('update:inputValue', ($event.target as HTMLInputElement)?.value)
      "
      :placeholder="placeholder"
      :type="inputType"
      :required="required"
    />
  </div>
</template>

<script setup lang="ts">
  interface Props {
    //it's nonsensical that TS complains about this
    //@ts-expect-error: TS2749
    inputType?: FormInputType;
    inputValue?: string;
    label: string | boolean;
    index: number;
    placeholder: string;
    required?: boolean;
  }

  withDefaults(defineProps<Props>(), {
    inputType: FormInputType.TEXT,
    inputValue: "",
    label: false,
    index: 0,
    required: false,
  });

  defineEmits(["update:inputValue"]);
</script>

<style lang="scss" scoped>
  label {
    font-size: $medium-large-text-size;
    font-weight: $header-text-weight;
    margin-bottom: 0.5rem;
  }

  .required {
    font-size: $small-text-size;
    font-weight: $thin-text-weight;
    color: $primary-red-color;
  }

  .control-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
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
