<script setup lang="ts">
import Input from '@/components/Input.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import type { ButtonProps } from '@/types/Props';
import { ref } from 'vue';
import { required, validate, smallerThan, largerThan, isValidLicensePlate } from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation';
import router from "@/router";
import { useCar } from '@/composables/useCar';


// composable functions
const { getEmptyCarCreate, createCar } = useCar()


// variables
const carCreate = getEmptyCarCreate()
const carCreateValidationSchema: ValidationSchema = {
  license_plate: [required('Kennzeichen'), isValidLicensePlate()],
  brand: [required('Hersteller')],
  model: [required('Modell')],
  n_seats: [required('Anzahl Sitzplätze'), largerThan(1, 'Mögliche Anzahl Sitze: 2-20'), smallerThan(21, 'Mögliche Anzahl Sitze: 2-20')],
  color: [required('Farbe')],
}
const errors = ref<Record<string, string[]>>({})


// functions
const tryCreateCar = async (): Promise<void> => {

  errors.value = validate(carCreate as Record<string, string>, carCreateValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    return
  }

  await createCar(carCreate);
  router.push('/signup/drivers_license');
}

// components
const hoverButtons: ButtonProps[] = [
  {variant: "primary", text: "Nächster Schritt", onClick: tryCreateCar},
  {variant: "tertiary", text: "Später", to: "/signup/drivers_license"},
]

</script>

<template>
  <div class="view-container">

    <PageTitle :goBack="true">Account einrichten 2/3</PageTitle>

    <p class="text-md text-bold margin-botton-l">Trage deine Autodetails ein, damit dich deine Mitfahrer rechtzeitig erkennen.</p>
    <div class="form-container">
      <div>
        <Input 
        type="text" 
        label="Kennzeichen" 
        v-model="carCreate.license_plate"
        :error="errors.license_plate?.[0]"
        />
        <p class="text-xs margin-top-s margin-left-md text-neutral-400">Eingabe mit Bindestrichen getrennt. Beispiel: BRB-TH-123</p>
      </div>
      <Input 
        type="text" 
        label="Hersteller" 
        v-model="carCreate.brand"
        :error="errors.brand?.[0]"
      />
      <Input 
        type="text" 
        label="Modell" 
        v-model="carCreate.model"
        :error="errors.model?.[0]"
      />
      <Input 
        type="number"
        label="Anzahl Sitzplätze" 
        v-model="carCreate.n_seats"
        :min="2"
        :max="20"
        :error="errors.n_seats?.[0]"
        />
      <Input 
        type="text" 
        label="Farbe" 
        v-model="carCreate.color"
        :error="errors.color?.[0]"
      />
    </div>

    <HoverButton :buttons="hoverButtons"/>
  </div>
</template>