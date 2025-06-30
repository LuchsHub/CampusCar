<script setup lang="ts">
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import type { ButtonProps } from '@/types/Props';
import type { Ride } from '@/types/Ride';
import { reactive, ref } from 'vue';
import { validate, required, isDate } from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation';

const ride = reactive<Ride>({
  id: ride.id,
  to: `${ride.end_location?.street}, ${ride.end_location?.postal_code} ${ride.end_location?.city}`,
  date: new Date(ride.arrival_time).toLocaleDateString('de-DE', { day: '2-digit', month: 'short' }),
  time: new Date(ride.arrival_time).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' }),
  price: ride.price?.toFixed(2) + ' €' || '4,50 €',
  image: 'https://randomuser.me/api/portraits/women/1.jpg'
})

const errors = ref<Record<string, string[]>>({})

const rideValidationSchema: ValidationSchema = {
  date: [required('Datum ist erforderlich'), isDate()],
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
  {variant: "primary", text: "Fahrt ", onClick: saveRide},
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