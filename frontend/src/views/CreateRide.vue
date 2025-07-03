<script setup lang="ts">
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import type { ButtonProps } from '@/types/Props';
import { ref, onMounted } from 'vue'
import { validate, required, largerThan, smallerThan } from '@/services/validation'
import { useRide } from '@/composables/useRide';
import { useLocation } from '@/composables/useLocation';
import { useUser } from '@/composables/useUser';
import { useToaster } from '@/composables/useToaster';
import type { RideCreateBase } from '@/types/Ride';
import type { LocationCreateDto } from '@/types/Location';
import router from '@/router';
import type { CarGet } from '@/types/Car';
import { useCar } from '@/composables/useCar';
import CarSelect from '@/components/CarSelect.vue';

const { getEmptyRideCreate, postRide } = useRide();
const { getLocationCreateValidationSchema, getEmptyLocationCreate } = useLocation();
const { getCurrentUserLocation } = useUser();
const { showToast } = useToaster();
const { getUserCarsData } = useCar();

// Variables 
const rideCreate: RideCreateBase = getEmptyRideCreate(); 
const rideCreateStartLocation: LocationCreateDto = getEmptyLocationCreate();
const rideCreateEndLocation: LocationCreateDto = getEmptyLocationCreate();
const userCars = ref<CarGet[]>([]);
const selectedCar = ref<CarGet | null>(null);

// set to true if no cars available after initial fetch 
// -> prevents error to show up for a short duration when cars are not fetched yet 
const showCarError = ref<boolean>(false);

const errorsRideCreate = ref<Record<string, string[]>>({})
const errorsStartLocation = ref<Record<string, string[]>>({})
const errorsEndLocation = ref<Record<string, string[]>>({})

// fetch data async from backend when component gets loaded
onMounted(async () => {
  userCars.value = await getUserCarsData();
  handleCarSelect(userCars.value[0]) // set first car as selected car
  
  if(!selectedCar.value){
    showCarError.value = true;
  }

  const location = await getCurrentUserLocation();
  if (location) {
    Object.assign(rideCreateStartLocation, location)
  }
})

// ensure responsitivity -> when selectedCar updates
const getRideValidationSchema = () => ({
  max_n_codrives: [
    required('Max. Mitfahrer'),
    largerThan(0, "Max. Mitfahrer muss größer als 0 sein."),
    smallerThan(
      Number(selectedCar.value?.n_seats),
      `Max. Mitfahrer für ausgewähltes Auto: ${Number(selectedCar.value?.n_seats) - 1}`
    )
  ],
  max_request_distance: [required('Max. Umweg'), largerThan(0, "Max. Umweg muss größer als 0 sein.")],
  arrival_date: [required('Tag')],
  arrival_time: [required('Ankunftszeit')],
});

const handleCarSelect = (car: CarGet | undefined) => {
  if (car) { // in case user has no car but inputs something into max_no_codrivers
    selectedCar.value = car;
    rideCreate.car_id = car.id;
    rideCreate.max_n_codrives = Number(car.n_seats)-1 // take driver into account
  }
}

const createRide = async (): Promise<void> => {
  errorsRideCreate.value = validate(rideCreate as Record<string, string>, getRideValidationSchema())
  errorsStartLocation.value = validate(rideCreateStartLocation as Record<string, string>, getLocationCreateValidationSchema())
  errorsEndLocation.value = validate(rideCreateEndLocation as Record<string, string>, getLocationCreateValidationSchema())
  
  // check form innput
  if (
    Object.keys(errorsRideCreate.value).length > 0 
    || Object.keys(errorsStartLocation.value).length > 0 
    || Object.keys(errorsEndLocation.value).length > 0) {
      return;
    }
    
  // check if a car is selected
  if (!selectedCar.value) {
    showToast('error', 'Füge zuerst ein Auto hinzu.')
    return;
  }

  try{
    await postRide(rideCreate, rideCreateStartLocation, rideCreateEndLocation);
    showToast("success", "Fahrt erstellt.")
    router.push("/my_rides");
  } catch (error: unknown){
    console.log(error);
    // reset form data
    Object.assign(rideCreate, getEmptyRideCreate());
    Object.assign(rideCreateStartLocation, getEmptyLocationCreate());
    Object.assign(rideCreateEndLocation, getEmptyLocationCreate());
  }
}

const addStop = ():void => {
  showToast("info", "Dieses Feature ist noch nicht implementiert.");
}

const hoverButtons: ButtonProps[] = [
  {variant: "primary", text: "Fahrt erstellen", onClick: createRide},
]
</script>

<template>
  <div class="view-container padding-bottom-hb-1">

    <PageTitle :goBack="true">Fahrt anbieten</PageTitle>
    <div v-if="userCars.length === 0  && showCarError" class="margin-botton-l error-message-container">
      <p class="text-danger">Du hast noch kein Auto hinterlegt. Füge zunächst ein Auto zu deinem Profil hinzu bevor du eine Fahrt erstellst.</p>
    </div>

    <h2>Abfahrt</h2>
    <div class="form-container">
      <Input 
        type="date" 
        label="Datum" 
        v-model="rideCreate.arrival_date"
        :error="errorsRideCreate.arrival_date?.[0]"
      />
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
        v-model="rideCreate.arrival_time"
        :error="errorsRideCreate.arrival_time?.[0]"
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
    <div class="form-container">
      <Input 
        type="number" 
        label="Max. Umweg (km)" 
        v-model="rideCreate.max_request_distance"
        :error="errorsRideCreate.max_request_distance?.[0]"
      />
      <Input 
        type="number" 
        label="Max. Mitfahrer" 
        v-model="rideCreate.max_n_codrives"
        :error="errorsRideCreate.max_n_codrives?.[0]"
      />
    </div>

    <h2>Auto</h2>
    <div v-if="userCars.length === 0" class="width-100">
      <!-- TODO: change route to go directly to the add car form -->
      <Button variant="secondary" @click="router.push('/profile')">
        Auto hinzufügen
      </Button>
    </div>
    <div v-else class="width-100">
      <template v-for="(car, index) in userCars" :key="car.id">
        <CarSelect
          :car="car"
          :selected="car.id === selectedCar?.id"
          @select="handleCarSelect"
        />
        <hr v-if="index < userCars.length - 1" />
      </template>
    </div>
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