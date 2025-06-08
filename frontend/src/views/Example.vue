<script setup lang="ts">
import Input from '../components/Input.vue';
import Button from '../components/Button.vue';
import HoverButton from '../components/HoverButton.vue';
import PageTitle from '../components/PageTitle.vue';
import type { ButtonProps } from '../types/Props';

const buttons: ButtonProps[] = [
  {variant: "primary", color: "primary", text: "Fahrt erstellen"},
]
</script>

<template>
  <div class="view-container">
    <PageTitle to="/">Fahrt anbieten</PageTitle>
    <h1></h1>
    <h2>Abfahrt</h2>
    <div class="form-container">
      <Input type="date" label="Datum"/>
      <Input type="time" label="Uhrzeit"/>
      <Input type="text" label="Ort"/>
    </div>
    <h2>Zwischenstopps</h2>
    <Button variant="secondary" color="primary">Zwischenstopp hinzufügen</Button>
    <h2>Ankunft</h2>
    <div class="form-container">
      <Input type="time" label="Uhrzeit"/>
      <Input type="text" label="Ort"/>
    </div>
    <h2>Optionen</h2>
    <HoverButton :buttons="buttons"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}

.form-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--horizontal-gap)
}
</style>