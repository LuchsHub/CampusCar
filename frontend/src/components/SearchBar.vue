<script setup lang="ts">
import { defineEmits, ref, watch } from 'vue'

const emit = defineEmits(['update:query'])

const query = ref('')

watch(query, (newVal) => {
  emit('update:query', newVal)
})
</script>

<template>
  <div class="search-bar">
    <i class="icon">🔍</i>
    <input
      type="text"
      v-model="query"
      class="input"
      placeholder="Wohin soll’s gehen?"
    />
  </div>
</template>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  background-color: var(--color-background-50, #f8f6f9);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-lg, 12px);
  box-shadow: var(--shadow-xs, 0 1px 2px rgba(0,0,0,0.05));
  margin: 1rem 0;
  cursor: text;
}

.icon {
  margin-right: 0.75rem;
  font-size: 1.2rem;
}

.input {
  border: none;
  background: transparent;
  outline: none;
  width: 100%;
  font-size: 1rem;
  color: var(--color-text-strong, #1e1b26);
}
</style>
