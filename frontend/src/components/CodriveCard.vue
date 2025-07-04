<script setup lang="ts">
import type { InputProps } from '../types/Props'

const props = withDefaults(defineProps<InputProps & { error?: string }>(), {
  placeholder: '-',
  error: ''
})

const emit = defineEmits(['update:modelValue', 'update:error'])

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
    padding: var(--input-padding-top) var(--container-padding-horizontal) var(--container-padding-vertical);
    border-radius: var(--border-radius);
    background-color: var(--color-neutral-200);
  }
</style>
  