<script setup lang="ts">
import Input from '../components/Input.vue';
</script>

<template>
  <div class="view-container">
    <h1>Beispiel</h1>
    <h2>Daten Eintragen 1</h2>
    <div class="container">
      <Input />
      <Input />
    </div>
    <h2>Daten Eintragen 2</h2>
    <div class="container">
      <Input />
      <Input />
      <Input />
    </div>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}

.container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--horizontal-gap)
}
</style>