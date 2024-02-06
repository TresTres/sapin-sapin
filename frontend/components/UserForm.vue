<template>
  <form class="pure-form-1-2 pure-form-aligned" @submit.prevent="handleSubmit">
    <fieldset class="pure-group">
      <span v-text="errorTextModel"></span>
      <div v-for="(controlGroup, index) in controlGroups">
        <UserFormInput
          :label="controlGroup.label"
          :index="index"
          :isPassword="controlGroup.isPassword"
          :placeholder="controlGroup.placeholder"
          v-model:inputValue="controlGroup.modelValue"
        />
        <p> 
          <span v-text="controlGroup.modelValue"></span>
        </p>
      </div>
    </fieldset>
    <button
      type="submit"
      class="pure-button pure-input-1-2 pure-button-primary"
    >
      {{ submitButtonText }}
    </button>
  </form>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const { handleSubmit, controlGroups, submitButtonText } = defineProps({
  handleSubmit: {
    type: Function as PropType<() => Promise<void>>,
    required: true,
  },
  controlGroups: {
    type: Array as PropType<
      {
        label: string;
        placeholder: string;
        isPassword?: boolean;
        modelValue: Ref<string>;
      }[]
    >,
    required: true,
  },
  submitButtonText: {
    type: String,
    required: true,
  },
});

const errorTextModel = defineModel("errorTextModel", {
  type: String,
  default: "",
});
</script>
