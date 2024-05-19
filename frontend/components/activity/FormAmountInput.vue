<!-- component that handles formatting numerical input from free text -->

<template>
  <div class="control-group">
    <label v-if="label" for="aligned-identifier">
      {{ `${deduction ? "Deduct" : "Add"} ${label}` }}
      <span v-if="required" class="required">*required</span>
    </label>
    <div class="formatted-amount">
      <div class="unit">{{ unitLabel }}</div>
      <input
        :id="`${label}-${index}-amount`"
        v-model="inputAmount"
        type="number"
        class="amount-field"
        :placeholder="placeholder"
        :required="required"
        min="0"
        step=".01"
        @change.prevent="(event) => handleAmountChange(event)"
      />
      <button class="toggle-button" @click.prevent="() => toggleDeduct()">
        {{ deduction ? "Add" : "Deduct" }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  unitLabel?: string;
  label: string | boolean;
  index?: number;
  placeholder: string;
  required?: boolean;
}

withDefaults(defineProps<Props>(), {
  unitLabel: "$",
  label: false,
  index: 0,
  required: false,
});

const convertAmount = (value: number): string => {
  /*
      Converts the input value to a float with 2 decimal places
    */
  return Math.abs(value).toFixed(2);
};

// true value controlled by model
const amountValue = defineModel<number>("amountValue", {
  required: true,
  default: 0,
});
// value displayed in input field
const inputAmount = ref<string>(convertAmount(amountValue.value));
const deduction = ref<boolean>(amountValue.value < 0);

watch(amountValue, (newValue) => {
  // upon model change, update input fields
  inputAmount.value = convertAmount(newValue);
  deduction.value = newValue < 0;
});

const toggleDeduct = (): void => {
  /*
      Toggles if the amount should be added or deducted
    */
  deduction.value = !deduction.value;
  calculateAmount();
};

const handleAmountChange = (event: Event): void => {
  /*
      Format the amount input to a float with two decimal places for display
    */

  const formattedValue = convertAmount(
    Math.max((event.target as HTMLInputElement).valueAsNumber, 0),
  );
  inputAmount.value = formattedValue;
  calculateAmount();
};

const calculateAmount = (): void => {
  /*
      Calculate the amount based on the input value and the deduction flag
    */
  const floatValue = parseFloat(inputAmount.value);
  amountValue.value = deduction.value ? -1 * floatValue : floatValue;
};
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

.formatted-amount {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  gap: 0.5rem;
}
.amount-field {
  @include text-input;
}

.unit {
  @include input-label;
  text-align: right;
  font-size: $large-text-size;
}

.toggle-button {
  @include small-button;
  min-width: 15%;
  @include hover-change-colors(
    $primary-orange-color,
    $light-orange-color,
    $white-color,
    $dark-orange-color
  );
}
</style>
