<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary'
  color?: 'primary' | 'danger'
  to?: string
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  color: 'primary',
  type: 'button',
  disabled: false
})

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const buttonClasses = computed(() => {
  const classes = ['button']
  
  // Add variant class
  classes.push(`button--${props.variant}`)
  
  // Add color class
  classes.push(`button--${props.color}`)
  
  // Add disabled class if needed
  if (props.disabled) {
    classes.push('button--disabled')
  }
  
  return classes.join(' ')
})

const handleClick = (event: MouseEvent) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<template>
  <component
    :is="to ? 'router-link' : 'button'"
    :to="to"
    :type="type"
    :class="buttonClasses"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot></slot>
  </component>
</template>

<style scoped>
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 35px;
  border-radius: 8px;
  font-family: Author;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  text-decoration: none;
  min-width: 120px;
}

/* Primary variant */
.button--primary {
  background-color: var(--color-primary-500);
  color: var(--color-neutral-100);
}

.button--primary:hover:not(.button--disabled) {
  background-color: var(--color-primary-900);
}

/* Secondary variant */
.button--secondary {
  background-color: var(--color-neutral-100);
  border: 2px solid var(--color-primary-500);
  color: var(--color-primary-500);
}

.button--secondary:hover:not(.button--disabled) {
  background-color: var(--color-primary-500-transparent);
}

/* Color variations */
.button--danger.button--primary {
  background-color: var(--color-support-danger-500);
}

.button--danger.button--primary:hover:not(.button--disabled) {
  background-color: var(--color-support-danger-500-transparent);
}

.button--danger.button--secondary {
  border-color: var(--color-support-danger-500);
  color: var(--color-support-danger-500);
}

.button--danger.button--secondary:hover:not(.button--disabled) {
  background-color: var(--color-support-danger-500-transparent);
}

/* Disabled state */
.button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style> 