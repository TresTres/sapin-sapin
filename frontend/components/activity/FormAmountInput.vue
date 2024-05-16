<!-- component that handles formatting numerical input from free text -->

<template>
  <div class="control-group">
    <label v-if="label" for="aligned-identifier">
      {{ label }}
      <span v-if="required" class="required">*required</span>
    </label>
    <div class="formatted-amount">
      <span>{{ unitLabel }}</span> 
      <input
        :id="`${label}-${index}-amount`"
        ref="amountField"
        class="amount-field"
        :placeholder="placeholder"
        :required="required"
        @change="(event: Event) => handleAmountInput(event)"
        @focus.stop="setCursorToStart()"
      />
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


  const amountField = ref<HTMLInputElement | null>(null);
  const amountValue = defineModel<number | string>("amountValue", {
    required: true,
    default: 0,
  });

  
  // watcher to handle outside model changes
  watch(amountValue, (newValue) => {
    if(typeof newValue === "number") {
      (amountField.value as HTMLInputElement).value = formatValue(newValue.toString());
    }
  });

  const setCursorToStart = (): void => {
    /*
      This function takes an input event and sets the cursor to the start of the input field.
      In some browsers, the focus event fires before the cursor is set, so we use setTimeout to ensure the cursor is set.
    */
    setTimeout(() => (amountField.value as HTMLInputElement).setSelectionRange(0, 0), .1);
  }

  const handleAmountInput = (event: Event): void => {
    /*
      This funciton takes an input event and formats the value to an internationalized float with two decimal places.
      It then updates the amountValue model with the numerical equivalent.
    */
    (event.target as HTMLInputElement).value = formatValue((event.target as HTMLInputElement)?.value);
    amountValue.value = convertToFloat((event.target as HTMLInputElement)?.value);
  }

  const formatValue = (value: string): string => {
    /*
      This function takes a string value and converts it to a internationalized
      float with two decimal places. If the value is not a number, it returns "0.00"
    */
    const parsedValue = convertToFloat(value);
    if(isNaN(parsedValue)) return "0.00";
    return Intl.NumberFormat("en-US", {
      style: "decimal",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
      minimumIntegerDigits: 1,
    }).format(parsedValue);
  };

  const convertToFloat = (value: string): number => {
    /*
      This function takes a string value and converts it to a numerical string with two decimal places.
      It removes any commas and spaces, and adds .00 to the end if the value is an integer.
      If the value is not a number, it returns 0.00
    */
    return parseFloat(value.replace(/(,)?(\s+)?/g, "") + ".00");
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
    align-items: center;
    gap: 0.5rem;

  }
  .amount-field {
    @include text-input;
  }
</style>