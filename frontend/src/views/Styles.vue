<script setup lang="ts">
import Button from '../components/Button.vue'
import Input from '../components/Input.vue'
</script>

<template>
  <div class="view-container">
    <div class="gap-container">
      <h1 class="margin-0">Heading 1</h1>
      <h2 class="margin-0">Heading 2</h2>
      <h3 class="margin-0">Heading 3</h3>
    </div>
    
    <h2>Primary Buttons</h2>
    <div class="gap-container">
      <Button variant="primary" color="primary">Default Primary</Button>
      <Button variant="primary" color="danger">Danger Primary</Button>
    </div>
    
    <h2>Secondary Buttons</h2>
    <div class="gap-container">
      <Button variant="secondary" color="primary">Default Secondary</Button>
      <Button variant="secondary" color="danger">Danger Secondary</Button>
    </div>
    
    <h2>Link Buttons</h2>
    <div class="gap-container">
      <Button variant="primary" color="primary" to="/">Home</Button>
      <Button variant="secondary" color="primary" to="/example">Example page</Button>
    </div>
    
    <h2>Input</h2>
    <div class="gap-container">
      <Input type="text" label="Input"/>
    </div>

    <h2>Text Examples</h2>
    <div class="gap-container">
      <p>Normal text</p>
      <p class="text-bold">Bold text</p>
      <p class="text-s">Small text</p>
      <p class="text-xs">Extra small text</p>
      <p class="text-primary">Primary text</p>
      <p class="text-info">Info text</p>
      <p class="text-warning">Warning text</p>
      <p class="text-danger">Danger text</p>
    </div>
  </div>
</template>

<style scoped>
.margin-0 {
  margin: 0
}

.button-demo {
  margin-top: 2rem;
}

.gap-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--horizontal-gap);
}

h2 {
  margin-bottom: 1rem;
}

h3 {
  margin-bottom: 0.5rem;
}
</style>