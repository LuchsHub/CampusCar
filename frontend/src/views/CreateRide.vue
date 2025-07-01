<script setup lang="ts">
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import type { ButtonProps } from '@/types/Props';
import { ref, onMounted } from 'vue'
import { validate, required, largerThan } from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation';
import { useRide } from '@/types/useRide';
import { useLocation } from '@/composables/useLocation';
import { useUser } from '@/composables/useUser';

const { getEmptyRideCreate } = useRide();
const { getLocationCreateValidationSchema, getEmptyLocationCreate } = useLocation();
const { getCurrentUserLocation } = useUser();

// Variables 
const rideCreate = getEmptyRideCreate(); 
const rideCreateStartLocation = getEmptyLocationCreate()
const rideCreateEndLocation = getEmptyLocationCreate()
console.log(rideCreateStartLocation)
onMounted(async () => {
  const location = await getCurrentUserLocation()
  if (location) {
    Object.assign(rideCreateStartLocation, location)
  }
})

const rideValidationSchema: ValidationSchema = {
    car_id: [required('Auto')],
    max_n_codrives: [required('Maximale Anzahl an Mitfahrern')],
    max_request_distance: [required('Maximaler Umweg'), largerThan(0, "Maximaler Umweg muss größer als 0 sein.")],
    time_of_arrival: [required('Ankunftszeit')]
}
const locationValidationSchema: ValidationSchema = getLocationCreateValidationSchema();
const errorsRideCreate = ref<Record<string, string[]>>({})
const errorsStartLocation = ref<Record<string, string[]>>({})
const errorsEndLocation = ref<Record<string, string[]>>({})

const createRide = ():void => {
  errorsRideCreate.value = validate(rideCreate as Record<string, string>, rideValidationSchema)
  errorsStartLocation.value = validate(rideCreateStartLocation as Record<string, string>, locationValidationSchema)
  errorsEndLocation.value = validate(rideCreateEndLocation as Record<string, string>, locationValidationSchema)
  if (
    Object.keys(errorsRideCreate.value).length > 0 
    && Object.keys(errorsEndLocation.value).length > 0 
    && Object.keys(errorsRideCreate.value).length > 0) {
    return
  }
  console.log(rideCreate);
}

const addStop = ():void => {
  console.log("addStop");
}

const hoverButtons: ButtonProps[] = [
  {variant: "primary", text: "Fahrt erstellen", onClick: createRide},
]
</script>

<template>
  <div class="view-container">

    <PageTitle :goBack="true">Fahrt anbieten</PageTitle>

    <h2>Abfahrt</h2>
    <div class="form-container">
      <!-- <Input 
        type="date" 
        label="Datum" 
        v-model="rideCreate.date"
        :error="errorsRideCreate.date?.[0]"
      /> -->
      <!-- <Input 
        type="time" 
        label="Uhrzeit" 
        v-model="rideCreate.time_of_departure"
        :error="errorsRideCreate.time_of_departure?.[0]"
      /> -->
      <Input 
        type="text" 
        label="Land" 
        v-model="rideCreateStartLocation.country"
        :error="errorsStartLocation.country?.[0]"
      />
      <Input 
        type="text" 
        label="Straße" 
        v-model="rideCreateStartLocation.street"
        :error="errorsStartLocation.street?.[0]"
      />
      <Input 
        type="text"
        label="Hausnummer" 
        v-model="rideCreateStartLocation.house_number"
        :error="errorsStartLocation.house_number?.[0]"
        />
      <Input 
        type="text" 
        label="Stadt" 
        v-model="rideCreateStartLocation.city"
        :error="errorsStartLocation.city?.[0]"
      />
      <Input 
        type="number" 
        label="PLZ" 
        v-model="rideCreateStartLocation.postal_code"
        :error="errorsStartLocation.postal_code?.[0]"
        :maxLength="5"
      />
    </div>
      
    <h2>Zwischenstopps</h2>
    <Button variant="secondary" :onClick="addStop">Zwischenstopp hinzufügen</Button>
    
    <h2>Ankunft</h2>
    <div class="form-container">
      <Input 
        type="time" 
        label="Uhrzeit" 
        v-model="rideCreate.time_of_arrival"
        :error="errorsRideCreate.time_of_arrival?.[0]"
      />
      <Input 
        type="text" 
        label="Land" 
        v-model="rideCreateEndLocation.country"
        :error="errorsEndLocation.country?.[0]"
      />
      <Input 
        type="text" 
        label="Straße" 
        v-model="rideCreateEndLocation.street"
        :error="errorsEndLocation.street?.[0]"
      />
      <Input 
        type="text"
        label="Hausnummer" 
        v-model="rideCreateEndLocation.house_number"
        :error="errorsEndLocation.house_number?.[0]"
        />
      <Input 
        type="text" 
        label="Stadt" 
        v-model="rideCreateEndLocation.city"
        :error="errorsEndLocation.city?.[0]"
      />
      <Input 
        type="number" 
        label="PLZ" 
        v-model="rideCreateEndLocation.postal_code"
        :error="errorsEndLocation.postal_code?.[0]"
        :maxLength="5"
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
</style>