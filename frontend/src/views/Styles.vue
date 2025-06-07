<script setup lang="ts">
import { ref } from 'vue'
import Button from '../components/Button.vue'

const handleClick = () => {
  console.log('Button clicked!')
}
</script>

<template>
  <main>
    <h1>CampusCar Styles</h1>

    <h1>Heading 1</h1>
    <h2>Heading 2</h2>
    <h3>Heading 3</h3>
    
    <h2>Button Examples</h2>
    
    <div class="button-group">
      <h3>Primary Buttons</h3>
      <Button @click="handleClick">Default Primary</Button>
      <Button color="danger" @click="handleClick">Danger Primary</Button>
      <Button disabled>Disabled Primary</Button>
    </div>

    <div class="button-group">
      <h3>Secondary Buttons</h3>
      <Button variant="secondary" @click="handleClick">Default Secondary</Button>
      <Button variant="secondary" color="danger" @click="handleClick">Danger Secondary</Button>
      <Button variant="secondary" disabled>Disabled Secondary</Button>
    </div>

    <div class="button-group">
      <h3>Link Buttons</h3>
      <Button to="/about">Link to About</Button>
      <Button variant="secondary" to="/contact">Link to Contact</Button>
    </div>

    <h3>Text Examples</h3>
    <p>Normal text</p>
    <p class="text-bold">Bold text</p>
    <p class="text-s">Small text</p>
    <p class="text-xs">Extra small text</p>
    <p class="text-primary">Primary text</p>
    <p class="text-info">Info text</p>
    <p class="text-warning">Warning text</p>
    <p class="text-danger">Danger text</p>

  </main>
</template>

<style scoped>
main {
  padding: 2rem;
  text-align: flex-start;
  align-items: flex-start;
}

.button-demo {
  margin-top: 2rem;
}

.button-group {
  margin: 2rem 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
}

h2 {
  margin-bottom: 1rem;
}

h3 {
  margin-bottom: 0.5rem;
}
</style>