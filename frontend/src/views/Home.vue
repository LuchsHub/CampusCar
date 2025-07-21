<script setup lang="ts">
import Map from '../components/Map.vue'
import SearchBar from '../components/SearchBar.vue'
import BottomSheet from '../components/BottomSheet.vue'
import { ref, computed, onMounted } from 'vue'
import type { RideGetDto } from '../types/Ride' // removed import for RideDto because of linting
import { useRide } from '@/composables/useRide'
import RideCard from '@/components/RideCard.vue'
import type { UserGet } from '@/types/User'
import { useUser } from '@/composables/useUser'

const { getAllRidesWithMaxDistance } = useRide();
const { getUserMe } = useUser()
const searchQuery = ref('')
const rides = ref<RideGetDto[]>([])
const sheetY = ref(0)
const currentUser = ref<UserGet | null>(null)

const filteredRides = computed(() => {
  const now = new Date()

  return rides.value.filter((ride) => {
    // Combine date & time
    const departureDateTime = new Date(`${ride.departure_date}T${ride.departure_time}`)

    return (
      ride.type === 'other' &&
      ride.driver.id !== currentUser.value?.id &&
      departureDateTime > now &&
      ride.end_location.city.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})

onMounted( async () => {
  rides.value = await getAllRidesWithMaxDistance(30);
  currentUser.value = await getUserMe()
})
</script>

<template>
  <div class="view-container">
    <div class="map-container" :style="{ height: `${sheetY}px` }">
      <Map :rides="filteredRides" />
    </div>

    <BottomSheet v-model="sheetY">
      <SearchBar v-model:query="searchQuery" />
      <div class="ride-list">
        <template v-for="(ride, index) in filteredRides" :key="ride.id">
          <RideCard :ride="ride"/>
          <hr v-if="index < filteredRides.length - 1" />
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
