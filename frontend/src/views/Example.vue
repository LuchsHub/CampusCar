<script setup lang="ts">
import Input from '../components/Input.vue';
import Button from '../components/Button.vue';
import HoverButton from '../components/HoverButton.vue';
import PageTitle from '../components/PageTitle.vue';
import type { ButtonProps } from '../types/Props';
import type { Ride } from '../types/Ride';
import { reactive, ref } from 'vue';
import { validate, required, isDate } from '../services/validation'
import type { ValidationSchema } from '../types/Validation';

const ride = reactive<Ride>({
  date: "",
  departureTime: "",
  departureLocation: "",
  arrivalTime: "",
  arrivalLocation: ""
})

const errors = ref<Record<string, string[]>>({})

const rideValidationSchema: ValidationSchema = {
  date: [required('Datum ist erforderlich'), isDate('Ungültiges Datum')],
  departureTime: [required('Abfahrtszeit ist erforderlich')],
  departureLocation: [required('Abfahrtsort ist erforderlich')],
  arrivalTime: [required('Ankunftszeit ist erforderlich')],
  arrivalLocation: [required('Ankunftsort ist erforderlich')],
}

const saveRide = ():void => {
  errors.value = validate(ride, rideValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    return
  }
  console.log(ride);
}

const hoverButtons: ButtonProps[] = [
  {variant: "primary", text: "Fahrt erstellen", onClick: saveRide},
]
</script>

<template>
  <div class="view-container">

    <PageTitle to="/">Fahrt anbieten</PageTitle>

    <h2>Abfahrt</h2>
    <div class="form-container">
      <Input 
        type="date" 
        label="Datum" 
        v-model="ride.date"
        :error="errors.date?.[0]"
      />
      <Input 
        type="time" 
        label="Uhrzeit" 
        v-model="ride.departureTime"
        :error="errors.departureTime?.[0]"
      />
      <Input 
        type="text" 
        label="Ort" 
        v-model="ride.departureLocation"
        :error="errors.departureLocation?.[0]"
        />
      </div>
      
      <h2>Zwischenstopps</h2>
      <Button variant="secondary">Zwischenstopp hinzufügen</Button>
      
      <h2>Ankunft</h2>
      <div class="form-container">
        <Input 
        type="time" 
        label="Uhrzeit" 
        v-model="ride.arrivalTime"
        :error="errors.arrivalTime?.[0]"
        />
        <Input 
        type="text" 
        label="Ort" 
        v-model="ride.arrivalLocation"
        :error="errors.arrivalLocation?.[0]"
      />
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

.error {
  color: var(--color-support-danger-500);
  font-size: var(--font-size-xs);
  margin-bottom: 0.5em;
}
</style>