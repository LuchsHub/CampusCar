<script setup lang="ts">
import Map from '../components/Map.vue'
import SearchBar from '../components/SearchBar.vue'
import BottomSheet from '../components/BottomSheet.vue'
import { ref, computed, onMounted } from 'vue'
import type { RideGetDto } from '../types/Ride'
import { useRide } from '@/composables/useRide'
import RideCardSelectable from '@/components/RideCardSelectable.vue'
import type { UserGet } from '@/types/User'
import { useUser } from '@/composables/useUser'
import { useMyRideStore } from '@/stores/MyRideStore'
import { useRouter } from 'vue-router'

const { getAllRidesWithMaxDistance } = useRide()
const { getUserMe } = useUser()
const searchQuery = ref('')
const rides = ref<RideGetDto[]>([])
const sheetY = ref(0)
const currentUser = ref<UserGet | null>(null)
const selectedRideId = ref<string | null>(null)
const lastClickedRideId = ref<string | null>(null)
const myRideStore = useMyRideStore()
const router = useRouter()

// Filter + Sortierung kombiniert
const filteredAndSortedRides = computed(() => {
  const now = new Date()
  const query = searchQuery.value.toLowerCase()

  const filtered = rides.value.filter((ride) => {
    const departureDateTime = new Date(`${ride.departure_date}T${ride.departure_time}`)
    const street = ride.end_location.street?.toLowerCase() || ''
    const city = ride.end_location.city?.toLowerCase() || ''
    const postalCode = ride.end_location.postal_code?.toString().toLowerCase() || ''

    return (
      ride.type === 'other' &&
      ride.driver.id !== currentUser.value?.id &&
      departureDateTime > now &&
      (street.includes(query) || city.includes(query) || postalCode.includes(query))
    )
  })

  if (selectedRideId.value) {
    const selected = filtered.find(r => r.id === selectedRideId.value)
    const others = filtered.filter(r => r.id !== selectedRideId.value)
    return selected ? [selected, ...others] : filtered
  }

  return filtered
})

// Klickverhalten
const handleRideSelect = (rideId: string) => {
  if (rideId === lastClickedRideId.value) {
    const ride = filteredAndSortedRides.value.find((r) => r.id === rideId)
    if (ride) {
      myRideStore.setRide(ride)
      router.push({ name: 'RideRequest' })
    }
  } else {
    selectedRideId.value = rideId
    lastClickedRideId.value = rideId
  }
}

onMounted(async () => {
  rides.value = await getAllRidesWithMaxDistance(30)
  currentUser.value = await getUserMe()
})
</script>

<template>
  <div class="view-container">
    <div class="map-container" :style="{ height: `${sheetY}px` }">
      <Map
        :rides="filteredAndSortedRides"
        :selectedRideId="selectedRideId"
        :bottomSheetHeight="sheetY"
      />
    </div>

    <BottomSheet v-model="sheetY">
      <SearchBar v-model:query="searchQuery" />
      <div class="ride-list">
        <template v-for="(ride, index) in filteredAndSortedRides" :key="ride.id">
          <RideCardSelectable
            :ride="ride"
            :selected="ride.id === selectedRideId"
            @rideSelected="handleRideSelect"
          />
          <hr v-if="index < filteredAndSortedRides.length - 1" />
        </template>
      </div>
    </BottomSheet>
  </div>
</template>

<style scoped>
.map-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  margin: 0 auto;
  width: 100%;
  max-width: 768px;
  transition: height 0.2s ease;
  z-index: 1;
}

.map-container :deep(#map) {
  width: 100% !important;
  height: 100% !important;
  border-radius: 12px;
}

.ride-list {
  display: flex;
  flex-direction: column;
  margin-top: 1rem;
}
</style>
