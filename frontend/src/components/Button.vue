<script setup lang="ts">
    import { computed } from 'vue'
    import type { ButtonProps } from '../types/Props';

    const props = defineProps<ButtonProps>() // Add loading prop

    const buttonClasses = computed(() => {
      const classes = ['button']
      classes.push(`button-${props.variant}`) // Add variant class
      if (props.disabled) {
        classes.push('button-disabled')
      } else {
        classes.push(`button-${props.color}`) // Add color class
      }
      return classes.join(' ')
    })

    const handleClick = ():void => {
      if (!props.to && props.onClick && !props.loading){ // Prevent click when loading
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
    :disabled="props.loading"
  >
    <span v-if="props.loading" class="spinner"/>
    <slot v-else/>
  </component>
</template>

<style scoped>
    .button {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 44px;
      padding: var(--button-padding-vertical) var(--button-padding-horizontal);
      border-radius: var(--border-radius);
      font-family: Author;
      font-size: var(--font-size-s);
      font-weight: var(--font-weight-semibold);
      cursor: pointer;
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
    
    /* Tertiary variant */
    .button-tertiary {
      background-color: transparent;
      border: none;
      color: var(--color-neutral-900);
      text-decoration: underline;
      box-shadow: none;
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

    .spinner {
      border: 2px solid #f3f3f3;
      border-top: 2px solid var(--color-primary-500);
      border-radius: 50%;
      width: var(--icon-xs);
      height: var(--icon-xs);
      animation: spin 0.8s linear infinite;
      display: inline-block;
      margin-right: 0.5em;
      vertical-align: middle;
    }
    @keyframes spin {
      0% { transform: rotate(0deg);}
      100% { transform: rotate(360deg);}
    }

    .button-disabled {
      background-color: var(--color-neutral-300, #e0e0e0);
      color: var(--color-neutral-500, #a0a0a0);
      border: none;
      pointer-events: none;
      box-shadow: none;
    }
</style> 