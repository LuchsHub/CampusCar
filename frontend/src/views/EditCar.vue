<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Input from '@/components/Input.vue'
import HoverButton from '@/components/HoverButton.vue'
import PageTitle from '@/components/PageTitle.vue'

import {
  required,
  validate,
  smallerThan,
  largerThan,
  isValidLicensePlate,
} from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation'

import { useCar } from '@/composables/useCar'
import { useToaster } from '@/composables/useToaster'
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal.vue'

// Setup
const route = useRoute()
const router = useRouter()
const carId = route.params.id as string

const { getUserCarsData, updateCar, deleteCar } = useCar()
const { showToast } = useToaster()

const showDeleteModal = ref(false)
const loading = ref(false);

// Car state
const carEdit = ref({
  license_plate: '',
  brand: '',
  model: '',
  n_seats: '',
  color: '',
})

// Validation
const errors = ref<Record<string, string[]>>({})

const schema: ValidationSchema = {
  license_plate: [required('Kennzeichen'), isValidLicensePlate()],
  brand: [required('Hersteller')],
  model: [required('Modell')],
  n_seats: [
    required('Anzahl Sitzplätze'),
    largerThan(1, 'Mögliche Anzahl Sitze: 2–20'),
    smallerThan(21, 'Mögliche Anzahl Sitze: 2–20'),
  ],
  color: [required('Farbe')],
}

// Load car data from localStorage
onMounted(async () => {
  try {
    const cars = await getUserCarsData()
    const car = cars.find(c => c.id === carId)
    if (!car) {
      showToast('error', 'Auto nicht gefunden.')
      router.push('/profile/edit')
      return
    }
    carEdit.value = {
      license_plate: car.license_plate,
      brand: car.brand,
      model: car.model,
      n_seats: car.n_seats.toString(),
      color: car.color,
    }
  } catch {
    showToast('error', 'Fehler beim Laden des Autos.')
    router.push('/profile/edit')
  }
})


// Update
const tryUpdateCar = async () => {
  errors.value = validate(carEdit.value as Record<string, string>, schema)
  if (Object.keys(errors.value).length > 0) return

  if (!carId) {
    showToast('error', 'Auto-ID fehlt.')
    return
  }

  loading.value = true;
  await updateCar(carId, carEdit.value)
  loading.value = false;
  showToast('success', 'Auto gespeichert.')
  router.push('/profile/edit')
}

// Delete
const onRequestDelete = () => {
  showDeleteModal.value = true
}

const onConfirmDelete = async () => {
  showDeleteModal.value = false
  loading.value = true;
  await deleteCar(carId)
  loading.value = false;
  showToast('success', 'Auto gelöscht.')
  router.push('/profile/edit')
}

const onCancelDelete = () => {
  showDeleteModal.value = false
}

</script>

<template>
  <div class="view-container padding-bottom-hb-1">
    <PageTitle :goBack="true">Auto bearbeiten</PageTitle>

    <div class="form-container">
      <Input
        type="text"
        label="Kennzeichen"
        v-model="carEdit.license_plate"
        :error="errors.license_plate?.[0]"
      />
      <p class="text-xs margin-top-s margin-left-md text-neutral-400">
        Eingabe mit Bindestrichen getrennt. Beispiel: BRB-TH-123
      </p>
      <Input
        type="text"
        label="Hersteller"
        v-model="carEdit.brand"
        :error="errors.brand?.[0]"
      />
      <Input
        type="text"
        label="Modell"
        v-model="carEdit.model"
        :error="errors.model?.[0]"
      />
      <Input
        type="number"
        label="Anzahl Sitzplätze"
        v-model="carEdit.n_seats"
        :min="2"
        :max="20"
        :error="errors.n_seats?.[0]"
      />
      <Input
        type="text"
        label="Farbe"
        v-model="carEdit.color"
        :error="errors.color?.[0]"
      />
    </div>

    <HoverButton
      :buttons="[
        { variant: 'primary', text: 'Speichern', onClick: tryUpdateCar, loading: loading },
        { variant: 'primary', text: 'Löschen', onClick: onRequestDelete , color: 'danger', loading: loading },
      ]"
    />
  </div>
  <ConfirmDeleteModal
    :open="showDeleteModal"
    subject="Auto"
    :requiresTextConfirmation="false"
    @confirm="onConfirmDelete"
    @cancel="onCancelDelete"
  />
</template>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
</style>
