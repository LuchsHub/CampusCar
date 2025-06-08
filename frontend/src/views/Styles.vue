<script setup lang="ts">
  import Button from '../components/Button.vue'
  import Input from '../components/Input.vue'
  import HoverButton from '../components/HoverButton.vue';
  import PageTitle from '../components/PageTitle.vue';
  import type { ButtonProps } from '../types/Props';

  const buttons: ButtonProps[] = [
    {variant: "primary", color: "primary", text: "Hoverbutton"},
  ]
</script>

<template>
  <div class="view-container"> <!--view-container is necessary in each view-->
    <div class="gap-container">
      <PageTitle to="/">Page Title Back</PageTitle>
      <PageTitle>Page Title</PageTitle>
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
      <Input type="text" label="Text"/>
      <Input type="number" label="Number"/>
      <Input type="email" label="Email"/>
      <Input type="password" label="Password"/>
      <Input type="time" label="Time"/>
      <Input type="date" label="Date"/>
    </div>

    <h2>Text Examples</h2>
    <div class="gap-container">
      <p>Medium text</p>
      <p class="text-s">Small text</p>
      <p class="text-xs">Extra small text</p>
      <p class="text-bold">Bold text</p>
      <p class="text-primary">Primary text</p>
      <p class="text-info">Info text</p>
      <p class="text-warning">Warning text</p>
      <p class="text-danger">Danger text</p>
    </div>

    <HoverButton :buttons="buttons"/> <!--HoverButtons do not need a container, they are positioned based on view-container-->
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
  gap: var(--horizontal-gap);
}

h2 {
  margin-bottom: 1rem;
}

h3 {
  margin-bottom: 0.5rem;
}
</style>