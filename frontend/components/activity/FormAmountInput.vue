<!-- component that handles formatting numerical input from free text -->

<template>
  <div class="control-group">
    <label v-if="label" for="aligned-identifier">
      {{ label }}
      <span v-if="required" class="required">*required</span>
    </label>
    <span>{{ unitLabel }}</span>
    <input
      :id="`${label}-${index}-amount`"
      class="amount-field"
      @change="(event: Event) => handleAmountInput(event)"
      :placeholder="placeholder"
      :required="required"
    />
  </div>
</template>

<script setup lang="ts">
  interface Props {
    unitLabel?: string;
    amountValue?: number;
    label: string | boolean;
    index: number;
    placeholder: string;
    required?: boolean;
  }

  withDefaults(defineProps<Props>(), {
    unitLabel: "$",
    amountValue: 0,
    label: false,
    index: 0,
    required: false,
  });

  const emit = defineEmits(["update:amountValue"]);


  const handleAmountInput = (event: Event) => {
    (event.target as HTMLInputElement).value = convertValue((event.target as HTMLInputElement)?.value);
    emit("update:amountValue", (event.target as HTMLInputElement).value);
  }

  const convertValue = (value: string): string => {
    const parsedValue = parseFloat(value.replace(/(,)?(\s+)?/g, "") + ".00");
    if(isNaN(parsedValue)) return "0.00";
    return Intl.NumberFormat("en-US", {
      style: "decimal",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
      minimumIntegerDigits: 1,
    }).format(parsedValue);
  };
</script>
