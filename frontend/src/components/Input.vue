<script setup lang="ts">
    import type { InputProps } from '../types/Props';


    const props = withDefaults(defineProps<InputProps>(), {
      placeholder: '-',
    })

    const emit = defineEmits(['update:modelValue'])

    const handleInput = (event: Event) => {
      const target = event.target as HTMLInputElement
      emit('update:modelValue', target.value)
    }
</script> 

<template>
    <div class="input-container">
        <input 
          :type="props.type" 
          :placeholder="props.placeholder"
          :value="props.modelValue"
          @input="handleInput"
        />
        <label>{{ props.label }}</label>
    </div>
</template>

  
<style scoped>
  .input-container {
    position: relative;
    width: 100%;
  }
  
  input {
    border: none;
    appearance: none;
    outline: none;
      
    width: 100%;
    padding: var(--input-padding-top) var(--input-padding-horizontal) var(--input-padding-bottom);
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
    padding: 0 0 0 var(--input-padding-horizontal);
    
    color: #aaa;
    background: var(--color-neutral-200);
    
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
</style>
  