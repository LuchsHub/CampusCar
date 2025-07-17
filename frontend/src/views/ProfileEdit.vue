<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '@/composables/useUser'
import { useToaster } from '@/composables/useToaster'
import { useCar } from '@/composables/useCar'
import { Check } from 'lucide-vue-next';
import { useAuthStore } from '@/stores/AuthStore'

import PageTitle from '@/components/PageTitle.vue'
import Input from '@/components/Input.vue'
import Button from '@/components/Button.vue'
import HoverButton from '@/components/HoverButton.vue'

import type { UserUpdate } from '@/types/User'
import type { CarGet } from '@/types/Car'
import { validate, required, isValidEmail, isTHBEmail, isValidPostalCode } from '@/services/validation'
import type { ValidationSchema } from "@/types/Validation"

const router = useRouter()
const authStore = useAuthStore();
const { getUserMe, getCurrentUserLocation, postUpdateUserData, uploadProfileImage, getProfileImageUrl } = useUser()
const { getUserCarsData } = useCar()
const { showToast } = useToaster()

const fileInputRef = ref<HTMLInputElement | null>(null)
const licenseFile = ref<File | null>(null)
const licenseUploaded = ref(false)
const profileImageFile = ref<File | null>(null)

// Profile
const profileImage = ref()
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

// Validaton Schema
const profileSchema: ValidationSchema = {
  firstName: [required('Vorname')],
  lastName: [required('Nachname')],
  email: [required('E-Mail'), isValidEmail(), isTHBEmail()],
  country: [required('Land')],
  street: [required('Straße')],
  houseNumber: [required('Hausnummer')],
  city: [required('Stadt')],
  postalCode: [required('PLZ'), isValidPostalCode()],
}

const errors = ref<Record<string, string[]>>({})
const loading = ref(false)

const handleCarSelect = (car: CarGet) => {
  router.push(`/profile/edit-car/${car.id}`)
}

const addCar = () => {
  router.push('/profile/add-car')
}

const triggerFileInput = () => {
  fileInputRef.value?.click()
}

const handleProfileImageChange = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  const validTypes = ['image/jpeg', 'image/png']
  if (!validTypes.includes(file.type)) {
    showToast('error', 'Nur .jpg, .jpeg oder .png Dateien sind erlaubt.')
    return
  }

  profileImageFile.value = file

  const reader = new FileReader()
  reader.onload = () => {
    profileImage.value = reader.result as string
  }
  reader.readAsDataURL(file)
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

    const imgUrl = await getProfileImageUrl(authStore.userId)
    profileImage.value = imgUrl ?? ""

    userCars.value = await getUserCarsData()
    selectedCar.value = userCars.value[0] || null
  } catch {
    showToast('error', 'Fehler beim Laden des Profils')
  }
}

const saveProfile = async () => {
  loading.value = true
  const values = {
    firstName: firstName.value,
    lastName: lastName.value,
    email: email.value,
    country: country.value,
    street: street.value,
    houseNumber: houseNumber.value,
    city: city.value,
    postalCode: postalCode.value,
  }

  const result = validate(values, profileSchema)

  if (Object.keys(result).length > 0) {
    errors.value = result
    showToast('error', 'Bitte überprüfe deine Eingaben.')
    loading.value = false
    return
  }

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
    location,
    has_license: licenseUploaded.value ? true : hasLicense.value
  }

  await postUpdateUserData(userUpdate)

  if (profileImageFile.value) {
    try {
      await uploadProfileImage(profileImageFile.value)
    } catch {
      showToast('error', 'Profilbild konnte nicht hochgeladen werden')
    }
  }

  router.push('/profile')
  loading.value = false
}

onMounted(() => {
  loadUserData()
})
</script>


<template>
  <div class="view-container">
    <PageTitle :goBack="true">Profil bearbeiten</PageTitle>

    <div class="profile-picture-section">
      <img
        :src="profileImage"
        class="profile-picture"
      />
      <input
        type="file"
        accept=".jpg,.jpeg,.png"
        ref="fileInputRef"
        style="display: none"
        @change="handleProfileImageChange"
      />
      <a class="change-link text-info" @click.prevent="triggerFileInput">Profilbild ändern</a>
    </div>

    <div class="form-container">
      <h2>Allgemein</h2>
      <Input type="text" label="Vorname" v-model="firstName" :error="errors.firstName?.[0]" />
      <Input type="text" label="Nachname" v-model="lastName" :error="errors.lastName?.[0]" />
      <Input type="text" label="E-Mail" v-model="email" :error="errors.email?.[0]" />
    </div>

    <div class="form-container">
      <h2>Abholdaten</h2>
      <Input type="text" label="Land" v-model="country" :error="errors.country?.[0]" />
      <Input type="text" label="Straße" v-model="street" :error="errors.street?.[0]" />
      <Input type="text" label="Hausnummer" v-model="houseNumber" :error="errors.houseNumber?.[0]" />
      <Input type="text" label="Stadt" v-model="city" :error="errors.city?.[0]" />
      <Input type="number" label="PLZ" v-model="postalCode" :error="errors.postalCode?.[0]" :maxLength="5"/>
    </div>

    <div class="form-container">
      <h2>Auto</h2>
      <div
        v-for="car in userCars"
        :key="car.id"
        class="car-entry"
        @click="() => handleCarSelect(car)"
      >
        <p class="car-license">{{ car.license_plate }}</p>
        <p class="car-model">{{ car.brand }} {{ car.model }} | {{ car.n_seats }} Sitzplätze</p>
      </div>
      <Button variant="secondary" @click="addCar">Auto hinzufügen</Button>
    </div>

    <div class="form-container">
      <h2>Führerschein</h2>
      <div v-if="!hasLicense">
        <Input
          type="file"
          label="Führerschein hochladen"
          :modelValue="''"
          @change="handleLicenseUpload"
        />
      </div>
      <div v-else class="license-info">
        <component :is="Check" class="icon-md text-primary"/>
        <p class="margin-left-md">
          Führerschein hinterlegt
        </p>
      </div>
    </div>

    <div class="form-container">
      <HoverButton :buttons="[{ variant: 'primary', text: 'Speichern', onClick: saveProfile, loading: loading }]" />
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
  justify-content: center;
  gap: 0.5rem;
  margin: 0 auto;
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

.text-info {
  color: var(--color-support-info-500);
}

.license-info {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
</style>
