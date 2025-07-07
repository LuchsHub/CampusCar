<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '@/composables/useUser'
import { useToaster } from '@/composables/useToaster'
import { useCar } from '@/composables/useCar'

import PageTitle from '@/components/PageTitle.vue'
import Input from '@/components/Input.vue'
import Button from '@/components/Button.vue'
import HoverButton from '@/components/HoverButton.vue'
import CarSelect from '@/components/CarSelect.vue'

import type { UserUpdate } from '@/types/User';
import type { CarGet } from '@/types/Car'

const router = useRouter()
const { getUserMe, getCurrentUserLocation, postUpdateUserData } = useUser()
const { getUserCarsData } = useCar()
const { showToast } = useToaster()

const fileInputRef = ref<HTMLInputElement | null>(null)
const licenseFile = ref<File | null>(null)
const licenseUploaded = ref(false)

// Profile
const profileImage = ref('https://randomuser.me/api/portraits/lego/1.jpg')
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const userName = ref('')
const hasLicense = ref(false)

// Location
const street = ref('')
const houseNumber = ref('')
const postalCode = ref('')
const city = ref('')
const country = ref('Deutschland')

// Cars
const userCars = ref<CarGet[]>([])
const selectedCar = ref<CarGet | null>(null)

const handleCarSelect = (car: CarGet) => {
  selectedCar.value = car
}

const addCar = () => {
  router.push('/profile/add-car')
}

const triggerFileInput = () => {
  fileInputRef.value?.click()
}

const handleProfileImageChange = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      profileImage.value = reader.result as string
    }
    reader.readAsDataURL(file)
  }
}

const handleLicenseUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    licenseFile.value = file
    licenseUploaded.value = true
  }
}

const loadUserData = async () => {
  try {
    const user = await getUserMe()
    firstName.value = user.first_name
    lastName.value = user.last_name
    email.value = user.email
    userName.value = user.user_name
    hasLicense.value = user.has_license

    const location = await getCurrentUserLocation()
    if (location) {
      street.value = location.street
      houseNumber.value = location.house_number
      postalCode.value = location.postal_code?.toString?.() || ''
      city.value = location.city
      country.value = location.country
    }

    userCars.value = await getUserCarsData()
    selectedCar.value = userCars.value[0] || null
  } catch {
    showToast('error', 'Fehler beim Laden des Profils')
  }
}

const saveProfile = async () => {
  const location = {
    street: street.value,
    house_number: houseNumber.value,
    postal_code: postalCode.value.toString(),
    city: city.value,
    country: country.value
  }

  const userUpdate: UserUpdate = {
    user_name: userName.value,
    first_name: firstName.value,
    last_name: lastName.value,
    email: email.value,
    location: location,
    has_license: licenseUploaded.value ? true : hasLicense.value
  }

  await postUpdateUserData(userUpdate)

  router.push('/profile')
}


onMounted(() => {
  loadUserData()
})
</script>

<template>
  <div class="view-container">
    <PageTitle :goBack="true">Profil bearbeiten</PageTitle>

    <div class="profile-picture-section">
      <img :src="profileImage" alt="Profilbild" class="profile-picture" />

      <!-- Verstecktes Datei-Input -->
      <input
        type="file"
        accept="image/*"
        ref="fileInputRef"
        style="display: none"
        @change="handleProfileImageChange"
      />

      <!-- Klickbarer Link -->
      <a class="change-link text-info" @click.prevent="triggerFileInput">Profilbild ändern</a>
    </div>

    <div class="form-container">
      <h2>Allgemein</h2>
      <Input type="text" label="Vorname" v-model="firstName" />
      <Input type="text" label="Nachname" v-model="lastName" />
      <Input type="text" label="E-Mail" v-model="email" disabled />
    </div>

    <div class="form-container">
      <h2>Abholdaten</h2>
      <Input type="text" label="Straße" v-model="street" />
      <Input type="text" label="Hausnummer" v-model="houseNumber" />
      <Input type="text" label="PLZ" v-model="postalCode" />
      <Input type="text" label="Stadt" v-model="city" />
    </div>

    <div class="form-container">
      <h2>Auto</h2>
      <CarSelect
        v-for="(car) in userCars"
        :key="car.id"
        :car="car"
        :selected="car.id === selectedCar?.id"
        @select="handleCarSelect"
      />
      <Button variant="secondary" @click="addCar">Auto hinzufügen</Button>
    </div>

    <!-- Nur ausblenden, wenn schon in der Datenbank vorhanden -->
    <div class="form-container" v-if="!hasLicense">
      <h2>Führerschein</h2>
      <Input
        type="file"
        label="Führerschein hochladen"
        :modelValue="''"
        @change="handleLicenseUpload"
      />
    </div>

    <div class="form-container">
      <HoverButton :buttons="[{ variant: 'primary', text: 'Speichern', onClick: saveProfile }]" />
    </div>
  </div>
</template>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 0 1rem 4rem;
}

.profile-picture-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* NEU */
  gap: 0.5rem;
  margin: 0 auto; /* zentriert horizontal */
}

.profile-picture {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.change-link {
  color: var(--color-primary);
  font-size: 0.875rem;
  text-decoration: underline;
  cursor: pointer;
  text-align: center;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-section :deep(.input-container) {
  width: 100%;
}

.text-info {
  color: var(--color-support-info-500);
}
</style>
