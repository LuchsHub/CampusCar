<script setup lang="ts">
    import { ref } from 'vue'
    import type { Ref } from 'vue'
    const content: Ref<string> = ref('')
</script> 

<template>
    <div class="input-container">
        <input type="text" v-model="content" placeholder="" />
        <label>Input</label>
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
      
    box-sizing: content-box;
    width: 100%;
    padding: var(--input-padding-top) var(--input-padding-horizontal) var(--input-padding-bottom);
    border-radius: var(--border-radius);
    background-color: var(--color-neutral-200);
    
    font-family: Author;
    font-size: 18px;
    font-weight: var(--font-weight-normal);
    color: var(--color-neutral-900);
  }
  
  input::placeholder {
    color: transparent; /* remove placeholder */
  }
  
  label {
    position: absolute;
    top: 50%;
    margin: 0;
    padding: 0 var(--input-padding-horizontal);
    
    color: #aaa;
    background: var(--color-neutral-200);
    
    font-family: Author;
    font-size: 18px;
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
    font-size: 14px;
    font-weight: var(--font-weight-normal);
    color: var(--color-neutral-400);
  }
</style>
  