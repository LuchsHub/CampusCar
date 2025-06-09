<script setup lang="ts">
  import Button from '../components/Button.vue'
  import Input from '../components/Input.vue'
  import HoverButton from '../components/HoverButton.vue';
  import PageTitle from '../components/PageTitle.vue';
  import type { ButtonProps } from '../types/Props';
  import { reactive } from 'vue';

  const exampleData = reactive({
    text: "",
    number: "",
    email: "",
    password: "",
    time: "",
    date: "",
  })

  const printExampleData = ():void => {
    console.log(exampleData);
  }
  
  const hoverButtons: ButtonProps[] = [
    {variant: "primary", text: "Hoverbutton", onClick:printExampleData},
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
      <Button variant="primary">Default Primary</Button>
      <Button variant="primary" color="danger">Danger Primary</Button>
    </div>
    
    <h2>Secondary Buttons</h2>
    <div class="gap-container">
      <Button variant="secondary">Default Secondary</Button>
      <Button variant="secondary" color="danger">Danger Secondary</Button>
    </div>
    
    <h2>Tertiary Button</h2>
    <div class="gap-container">
      <Button variant="tertiary">Default Tertiary</Button>
    </div>
    
    <h2>Link Buttons</h2>
    <div class="gap-container">
      <Button variant="primary" to="/">Example page</Button>
      <Button variant="secondary" to="/example">Example page</Button>
      <Button variant="tertiary" to="/example">Example page</Button>
    </div>
    
    <h2>Inputs</h2>
    <div class="gap-container">
      <Input type="text" label="Text" v-model="exampleData.text"/>
      <Input type="number" label="Number" v-model="exampleData.number"/>
      <Input type="email" label="Email" v-model="exampleData.email"/>
      <Input type="password" label="Password" v-model="exampleData.password"/>
      <Input type="time" label="Time" v-model="exampleData.time"/>
      <Input type="date" label="Date" v-model="exampleData.date"/>
    </div>

    <h2>Text Styles</h2>
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

    <HoverButton :buttons="hoverButtons"/> <!--HoverButtons do not need a container, they are positioned based on view-container-->
  </div>
</template>

<style scoped>
.margin-0 {
  margin: 0
}

.gap-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--horizontal-gap);
}
</style>