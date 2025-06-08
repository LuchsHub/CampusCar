<script setup lang="ts">
import Input from '../components/Input.vue';
import Button from '../components/Button.vue';
import HoverButton from '../components/HoverButton.vue';
import PageTitle from '../components/PageTitle.vue';
import type { ButtonProps } from '../types/Props';
import type { Ride } from '../types/Ride';
import { reactive } from 'vue';

const ride = reactive<Ride>({
  date: "",
  departureTime: "",
  departureLocation: "",
  arrivalTime: "",
  arrivalLocation: ""
})

const saveRide = ():void => {
  console.log(ride);
}

// Buttons to use as Hover Buttons 
const hoverButtons: ButtonProps[] = [
  {variant: "primary", color: "primary", text: "Fahrt erstellen", onClick: saveRide},
]
</script>

<template>
  <div class="view-container">
    <PageTitle to="/">Fahrt anbieten</PageTitle>
    <h2>Abfahrt</h2>
    <div class="form-container">
      <Input type="date" label="Datum" v-model="ride.date"/>
      <Input type="time" label="Uhrzeit" v-model="ride.departureTime"/>
      <Input type="text" label="Ort" v-model="ride.departureLocation"/>
    </div>
    <h2>Zwischenstopps</h2>
    <Button variant="secondary" color="primary">Zwischenstopp hinzufügen</Button>
    <h2>Ankunft</h2>
    <div class="form-container">
      <Input type="time" label="Uhrzeit" v-model="ride.arrivalTime"/>
      <Input type="text" label="Ort" v-model="ride.arrivalLocation"/>
    </div>
    <h2>Optionen</h2>
    <HoverButton :buttons="hoverButtons"/>
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