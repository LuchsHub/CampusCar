<script setup lang="ts">
    import { computed } from 'vue'
    import type { ButtonProps } from '../types/Props';

    const props = defineProps<ButtonProps>()

    const buttonClasses = computed(() => {
      const classes = ['button']
      classes.push(`button-${props.variant}`) // Add variant class
      classes.push(`button-${props.color}`) // Add color class
      return classes.join(' ')
    })

    const handleClick = ():void => {
      if (!props.to && props.onClick){
        props.onClick()
      }
    }
</script>

<template>
  <component
    :is="props.to ? 'router-link' : 'button'"
    :to="props.to"
    :class="buttonClasses"
    @click="handleClick"
  >
    <slot/>
  </component>
</template>

<style scoped>
    .button {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      padding: var(--button-padding-vertical) var(--button-padding-horizontal);
      border-radius: var(--border-radius);
      font-family: Author;
      font-size: var(--font-size-s);
      font-weight: var(--font-weight-semibold);
      cursor: pointer;
      text-decoration: none;
    }

    /* Primary variant */
    .button-primary {
      border: none;
      background-color: var(--color-primary-500);
      color: var(--color-neutral-900);
      box-shadow: 0 1px 10px var(--color-primary-500-transparent);
    }
    
    /* Secondary variant */
    .button-secondary {
      background-color: var(--color-neutral-100);
      border: 2px solid var(--color-primary-500);
      color: var(--color-primary-500);
    }
    
    /* Color variations */
    .button-danger.button-primary {
      background-color: var(--color-support-danger-500);
      box-shadow: 0 1px 10px var(--color-support-danger-500-transparent);
    }
    
    .button-danger.button-secondary {
      border-color: var(--color-support-danger-500);
      color: var(--color-support-danger-500);
      box-shadow: 0 1px 10px var(--color-support-danger-500-transparent);
    }
</style> 