<script setup lang="ts">
  import Button from './Button.vue'
  import type { HoverButtonProps } from '../types/Props'
  import { useRoute } from 'vue-router'
  import { useKeyboardVisible, isKeyboardVisible } from '@/composables/useKeyboardVisible';
  
  useKeyboardVisible();
  const route = useRoute()
  const props = defineProps<HoverButtonProps>()
</script>

<template>
    <div
      class="hover-button-container" 
      :class="route.meta.hideTabBar || isKeyboardVisible ? 'low-hover-button' : 'high-hover-button'"
    >
        <Button 
            v-for="(button, i) in props.buttons"
            :key="i"
            v-bind="button"
        >
            {{ button.text }}
        </Button>
    </div>
</template>

<style scoped>
.hover-button-container {
    display: flex;
    flex-direction: column;
    gap: var(--horizontal-gap);
    position: fixed;
    width: calc(100% - 60px);  /* 40px = 2*var(--app-padding-horizontal), but var() is not allowed inside of calc */
    margin: auto;
    left: 0;
    right: 0;
}

@media (min-width: 768px) {
  .hover-button-container {
    width: calc(700px - 60px); /* 700px = var(--tablet-content-max-width), 40px = var(--app-padding-horizontal) */
  }
}

@media (min-width: 1200px) {
  .hover-button-container {
    width: calc(900px - 60px); /* 900px = var(--desktop-content-max-width), 40px = var(--app-padding-horizontal) */
  }
}
</style>