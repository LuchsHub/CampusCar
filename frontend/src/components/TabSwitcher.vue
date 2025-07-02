<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import type { TabSwitcherProps } from '@/types/Props'

const props = defineProps<TabSwitcherProps>();

const emit = defineEmits(['update:modelValue']);
function selectTab(tab: string) {
  emit('update:modelValue', tab);
}
</script>

<template>
  <div class="tab-bar">
    <span
      v-for="tab in props.tabs"
      :key="tab"
      :class="{ active: tab === modelValue }"
      @click="selectTab(tab)"
    >{{ tab }}</span>
  </div>
</template>

<style scoped>
.tab-bar {
    display: flex;
    gap: 1rem;
    border-bottom: var(--line-width-s) solid var(--color-neutral-300);
    margin-bottom: var(--horizontal-gap);
    width: 100%;
}
.tab-bar span {
    font-family: Author, sans-serif;
    padding: 0.5rem 0;
    margin-bottom: calc(-1 * var(--line-width-s)); /* ensure border sith flush with surrounding div */
    font-weight: var(--font-weight-semibold);
    border-bottom: var(--line-width-m) solid transparent;
    color: var(--color-neutral-300);
transition: color 0.2s, border-bottom 0.2s;
}
.tab-bar span.active {
    font-weight: var(--font-weight-bold);
    color: var(--color-primary-500);
    border-bottom: var(--line-width-m) solid var(--color-primary-500);
}
</style>