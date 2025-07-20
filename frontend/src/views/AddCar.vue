<script setup lang="ts">
import Input from '@/components/Input.vue'
import HoverButton from '@/components/HoverButton.vue'
import PageTitle from '@/components/PageTitle.vue'
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
const loading = ref(false);

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

  loading.value = true;
  await createCar(carCreate)
  loading.value = false;
  router.push('/profile/edit') // Ziel nach dem Anlegen
}

// Buttons
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
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

    <HoverButton :buttons="[{ variant: 'primary', text: 'Speichern', onClick: tryCreateCar, loading: loading}]" />
  </div>
</template>

<style scoped>
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
