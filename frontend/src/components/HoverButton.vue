<script setup lang="ts">
  import Button from './Button.vue'
  import type { HoverButtonProps } from '../types/Props'

  const props = defineProps<HoverButtonProps>()
</script>

<template>
    <div class="hover-button-container">
        <Button 
            v-for="(button, i) in props.buttons"
            :key="i"
            :variant=button.variant
            :color=button.color
        >
            {{ button.text }}
        </Button>
    </div>
</template>

<style scoped>
.hover-button-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: var(--horizontal-gap);
    position: sticky;
    bottom: calc(var(--nav-min-height) + var(--hover-button-nav-margin));
}
</style>