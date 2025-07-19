<script setup lang="ts">
import type { InputProps } from '../types/Props'

const props = withDefaults(defineProps<InputProps & { error?: string }>(), {
  placeholder: '-',
  error: ''
})

const emit = defineEmits(['update:modelValue', 'update:error', 'blur'])

function onBlur(event: FocusEvent) {
  emit('blur', event);
}

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  let value = target.value
  
  // Apply maxLength limit if specified
  if (props.maxLength && value.length > props.maxLength) {
    value = value.slice(0, props.maxLength)
    // Update the input element's value to reflect the truncation
    target.value = value
  }
  
  emit('update:modelValue', value)
}
</script>

<template>
  <div>
    <div class="input-container">
      <input
        :type="props.type"
        :placeholder="props.placeholder"
        :value="props.modelValue"
        :maxlength="props.maxLength"
        @input="handleInput"
        @blur="onBlur"
        :class="{ 'input-error': !!props.error }"
      />
      <label>{{ props.label }}</label>
    </div>
    <p v-if="props.error" class="text-s text-danger margin-top-s margin-left-md">{{ props.error }}</p>
  </div>
</template>

  
<style scoped>
  .input-container {
    width: 100%;
    position: relative;
  }
  
  input {
    border: none;
    appearance: none;
    outline: none;
      
    width: 100%;
    padding: var(--input-padding-top) var(--container-padding-horizontal) var(--container-padding-vertical);
    border-radius: var(--border-radius);
    background-color: var(--color-neutral-200);
    
    font-family: Author;
    font-size: var(--font-size-md);
    font-weight: var(--font-weight-normal);
    color: var(--color-neutral-900);
  }
  
  input::placeholder {
    color: transparent; /* remove placeholder */
  }
  
  label {
    position: absolute;
    top: 50%;
    left: 0;
    margin: 0;
    padding: 0 0 0 var(--container-padding-horizontal);
    
    color: #aaa;
    
    font-family: Author;
    font-size: var(--font-size-md);
    color: var(--color-neutral-900);
    font-weight: var(--font-weight-normal);

    transform: translateY(-50%);
    pointer-events: none;
    transition: 0.2s ease all;
  }
  
  /* Put label above if input is focused or contains content */
  input:focus + label,
  input:not(:placeholder-shown) + label {
    top: 14px;
    font-family: Author;
    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-normal);
    color: var(--color-neutral-400);
  }

  .input-error {
    border: var(--line-width-m) solid var(--color-support-danger-500);
  }
</style>
  