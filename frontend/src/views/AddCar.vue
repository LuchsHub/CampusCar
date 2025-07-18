<script setup lang="ts">
import Input from '@/components/Input.vue'
import HoverButton from '@/components/HoverButton.vue'
import PageTitle from '@/components/PageTitle.vue'
import type { ButtonProps } from '@/types/Props'
import { ref } from 'vue'
import { useCar } from '@/composables/useCar'
import router from '@/router'

import {
  required,
  validate,
  smallerThan,
  largerThan,
  isValidLicensePlate
} from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation'

// Car logic
const { getEmptyCarCreate, createCar } = useCar()
const carCreate = getEmptyCarCreate()

// Validation
const carCreateValidationSchema: ValidationSchema = {
  license_plate: [required('Kennzeichen'), isValidLicensePlate()],
  brand: [required('Hersteller')],
  model: [required('Modell')],
  n_seats: [
    required('Anzahl Sitzplätze'),
    largerThan(1, 'Mögliche Anzahl Sitze: 2–20'),
    smallerThan(21, 'Mögliche Anzahl Sitze: 2–20')
  ],
  color: [required('Farbe')],
}
const errors = ref<Record<string, string[]>>({})

// Actions
const tryCreateCar = async (): Promise<void> => {
  errors.value = validate(carCreate as Record<string, string>, carCreateValidationSchema)
  if (Object.keys(errors.value).length > 0) return

  await createCar(carCreate)
  router.push('/profile/edit') // Ziel nach dem Anlegen
}

// Buttons
const buttons: ButtonProps[] = [
  { variant: 'primary', text: 'Speichern', onClick: tryCreateCar }
]
</script>

<template>
  <div class="view-container">
    <PageTitle :goBack="true">Auto hinzufügen</PageTitle>

    <div class="form-container">
      <div>
        <Input
          type="text"
          label="Kennzeichen"
          v-model="carCreate.license_plate"
          :error="errors.license_plate?.[0]"
        />
        <p class="text-xs margin-top-s margin-left-md text-neutral-400">
          Eingabe mit Bindestrichen getrennt. Beispiel: BRB-TH-123
        </p>
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

    <HoverButton :buttons="buttons" />
  </div>
</template>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 0 1rem 4rem;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.text-bold {
  font-weight: bold;
}

.margin-botton-l {
  margin-bottom: 1.5rem;
}
</style>
