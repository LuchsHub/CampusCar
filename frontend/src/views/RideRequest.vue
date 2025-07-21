<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue'
import HoverButton from '@/components/HoverButton.vue'
import LocationItem from '@/components/LocationItem.vue'
import Input from '@/components/Input.vue'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMyRideStore  } from '@/stores/MyRideStore'
import { useUser } from '@/composables/useUser'
import { sortLocationItemPropsByTimeAsc } from '@/services/utils'
import api from '@/services/api'
import { useToaster } from '@/composables/useToaster'
import InformationItem from '@/components/InformationItem.vue'
import ProfileCard from '@/components/ProfileCard.vue'
import { useCodrive } from '@/composables/useCodrive'

import type { LocationItemProps } from '@/types/Props'

import type { ValidationSchema } from "@/types/Validation"
import { validate, required, isValidPostalCode, largerThan, smallerThan } from '@/services/validation'
import type { LocationCreateDto } from '@/types/Location'

const router = useRouter()
const rideStore = useMyRideStore()
const { showToast } = useToaster()
const { getCurrentUserLocation } = useUser()
const { previewCodriveCost } = useCodrive();

const ride = computed(() => rideStore.ride)
const driver = computed(() => rideStore.ride?.driver)

if (!ride.value) router.push({ name: 'home' })

// const isRecurring = ref(false)
// const selectedDays = ref<string[]>([])

// const weekdays = [
//   { key: 'mo', label: 'Mo' },
//   { key: 'di', label: 'Di' },
//   { key: 'mi', label: 'Mi' },
//   { key: 'do', label: 'Do' },
//   { key: 'fr', label: 'Fr' },
//   { key: 'sa', label: 'Sa' },
//   { key: 'so', label: 'So' }
// ]

// function toggleDay(dayKey: string) {
//   if (selectedDays.value.includes(dayKey)) {
//     selectedDays.value = selectedDays.value.filter(d => d !== dayKey)
//   } else {
//     selectedDays.value.push(dayKey)
//   }
// }

const rideLocationItems = computed<LocationItemProps[]>(() => {
  if (!ride.value) return []
  const items: LocationItemProps[] = [
    {
      location: ride.value.start_location,
      arrival_time: ride.value.departure_time,
      arrival_date: ride.value.departure_date
    },
    ...ride.value.codrives.map(codrive => ({
      location: codrive.location,
      arrival_time: codrive.arrival_time,
      user: codrive.user
    })),
    {
      location: ride.value.end_location,
      arrival_time: ride.value.arrival_time,
      arrival_date: ride.value.arrival_date
    }
  ]
  return sortLocationItemPropsByTimeAsc(items)
})

// Mitfahrtanfrage
const message = ref('')
const seats = ref<number>(0)

const errors = ref<Record<string, string[]>>({})
const locationError = ref<boolean>(false);
const loading = ref<boolean>(false);

// Location
const street = ref('')
const houseNumber = ref('')
const postalCode = ref('')
const city = ref('')
const country = ref('Deutschland')
const estimatedCost = ref(0);

const calculateEstimatedCost = async () => {
  if (street.value && houseNumber.value && postalCode.value && city.value && country.value && ride.value) {
    try {
      loading.value = true;
      const result = await previewCodriveCost(ride.value.id, {
        'country': country.value,
        'postal_code': postalCode.value,
        'city': city.value,
        'street': street.value,
        'house_number': houseNumber.value,
      } as LocationCreateDto)
      estimatedCost.value = result
      locationError.value = false;
    } catch (error: unknown) {
      console.log(error);
      locationError.value = true;
      estimatedCost.value = 0;
    } finally {
      loading.value = false;
    }
  } else {
    estimatedCost.value = 0;
  } 

};

// Validaton Schema
const codriveValidationSchema: ValidationSchema = {
  country: [required('Land')],
  postalCode: [required('PLZ'), isValidPostalCode()],
  city: [required('Stadt')],
  street: [required('Straße')],
  houseNumber: [required('Hausnummer')],
  seats: [required('Anzahl Plätze'), largerThan(0, 'Anzahl Plätze muss größer als 0 sein.'), ...(ride.value ? [smallerThan(ride.value.n_available_seats+1, 'Zu viele Sitzplätze.')] : [])]
}

const loadLocation = async () => {
  try {
    const location = await getCurrentUserLocation()
    if (location) {
      street.value = location.street
      houseNumber.value = location.house_number
      postalCode.value = location.postal_code?.toString?.() || ''
      city.value = location.city
      country.value = location.country
      await calculateEstimatedCost();
    }
  } catch {
    showToast('error', 'Fehler beim Laden des Profils')
  }
}

const sendCodriveRequest = async () => {
  if (!ride.value) return

  const values = {
    country: country.value,
    street: street.value,
    houseNumber: houseNumber.value,
    city: city.value,
    postalCode: postalCode.value,
    seats: seats.value.toString(),
  }

  errors.value = validate(values as Record<string, string>, codriveValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    return
  }

  const location = {
    street: street.value,
    house_number: houseNumber.value,
    postal_code: postalCode.value.toString(),
    city: city.value,
    country: country.value
  }

  if (!location) {
    showToast('error', 'Kein Standort im Profil gefunden.')
    return
  }

  const fullMessage = message.value

  try {
    loading.value = true;
    await api.post(`/codrives/${ride.value.id}`, {
      location: location,
      message: fullMessage,
      n_passengers: seats.value
    })
    showToast('success', 'Anfrage erfolgreich gesendet.')
    router.push('/home')
  } catch {
    showToast('error', 'Anfrage fehlgeschlagen.')
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  loadLocation()
})
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
    <PageTitle :goBack="true">{{ 'Mitfahrt anfragen' }}</PageTitle>

    <!-- Fahrerinfo -->
    <h2>Fahrer</h2>
    <ProfileCard v-if="driver && ride"
      :first_name="driver.first_name"
      :last_name="driver.last_name"
      :avg_rating="driver.avg_rating"
      :profile_picture="ride.image"
    />

    <h2>Fahrtverlauf</h2>
    <div class="component-list">
      <LocationItem
        v-for="item in rideLocationItems"
        :key="item.arrival_time + item.location.city"
        :location="item.location"
        :arrival_time="item.arrival_time"
        :arrival_date="item.arrival_date"
        :user="item.user"
      />
    </div>

    <h2>Abholort</h2>
    
    <div class="form-container">
      <Input type="text" label="Straße" v-model="street" @blur="calculateEstimatedCost" :error="errors.street?.[0]"/>
      <Input type="text" label="Hausnummer" v-model="houseNumber" @blur="calculateEstimatedCost" :error="errors.houseNumber?.[0]"/>
      <Input type="text" label="PLZ" v-model="postalCode" :maxLength="5" @blur="calculateEstimatedCost" :error="errors.postalCode?.[0]"/>
      <Input type="text" label="Stadt" v-model="city" @blur="calculateEstimatedCost" :error="errors.city?.[0]"/>
      <Input type="text" label="Land" v-model="country" @blur="calculateEstimatedCost" :error="errors.country?.[0]"/>
      <div v-if="locationError" class="margin-botton-l error-message-container">
        <p class="text-danger">Ungültiger Abholort. Bitte prüfe deine Adresseingabe auf Fehler. Möglicherweise akzeptiert der Fahrer keine Umwege dieser Länge.</p>
      </div>
    </div>

    <h2>Mitfahrt Optionen</h2>
    <div class="form-container">
      <Input
      type="number"
      label="Anzahl Plätze"
      v-model.number="seats"
      :max="ride?.n_available_seats"
      min="1"
      required
      placeholder="Plätze anfragen"
      :error="errors.seats?.[0]"
      />
      
      <Input
        type="text"
        label="Nachricht (optional)"
        v-model="message"
        placeholder="Schreib dem Fahrer z.B. wo du zusteigst oder warum du mitfahren möchtest..."
      />
  
      <!-- Wiederholte Mitfahrt Checkbox -->
      <!-- <div class="repeat-block">
        <label class="repeat-checkbox">
          <input type="checkbox" v-model="isRecurring" />
          <span>Wiederholte Mitfahrt</span>
          <span class="info-icon" title="Diese Fahrt wird regelmäßig angeboten"/>
        </label>
  
        <div v-if="isRecurring" class="weekday-toggle">
          <div
            v-for="day in weekdays"
            :key="day.key"
            class="weekday"
            :class="{ active: selectedDays.includes(day.key) }"
            @click="toggleDay(day.key)"
          >
            <span>{{ day.label }}</span>
          </div>
        </div>
      </div> -->
    </div>


    <h2>Fahrtinformationen</h2>
    <div class="component-list">
      <InformationItem v-if="ride?.max_request_distance"
        type=pointCost
        :value="(estimatedCost/100).toFixed(2)"
      />
      <InformationItem
        type=availableSeats
        :value=ride?.n_available_seats
      />
    </div>

    <HoverButton :buttons="[
      {
        text: 'Mitfahrt anfragen',
        variant: 'primary',
        onClick: sendCodriveRequest,
        loading: loading,
        disabled: ride?.n_available_seats === 0 || locationError
      }
    ]" />
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
.ride-info {
  width: 100%;
}
.ride-info {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.info-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.info-icon {
  width: 24px;
  height: 24px;
  color: #1c1120;
}
.info-text {
  display: flex;
  flex-direction: column;
}
.info-label {
  font-size: 0.75rem;
  color: var(--color-neutral-500);
}
.repeat-block {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.repeat-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: bold;
}
.weekday-toggle {
  display: flex;
  gap: 0.5rem;
}
.weekday {
  padding: 0.5rem 0.75rem;
  border-radius: 12px;
  background: #f0edf4;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
  user-select: none;
}
.weekday.active {
  background: #1c1120;
  color: white;
}
</style>
