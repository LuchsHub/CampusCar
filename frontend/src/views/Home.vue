<script setup lang="ts">
import Map from '../components/Map.vue'
import SearchBar from '../components/SearchBar.vue'
import RideCardLaurin from '@/components/RideCardLaurin.vue'
import HoverButton from '../components/HoverButton.vue'
import BottomSheet from '../components/BottomSheet.vue'

import { ref, computed, onMounted } from 'vue'
// import { fetchRidesFromApi } from '../services/rides'
import type { RideCardData } from '../types/Ride' // removed import for RideDto because of linting
import { useToaster } from '@/composables/useToaster'
import { useRide } from '@/composables/useRide'
import { useAuthStore } from '@/stores/AuthStore'
import type { RideGet } from '../types/Ride'


const authStore = useAuthStore();
const { getRidesForUser } = useRide();
const { showToast } = useToaster()
const searchQuery = ref('')
const rides = ref<RideCardData[]>([])
const sheetY = ref(0)

const fetchRides = async () => {
  try {
    // const data: RideDto[] = await fetchRidesFromApi()
    const data: RideGet[] = await getRidesForUser(authStore.userId);
    rides.value = data.map((ride): RideCardData => ({
      id: Number(ride.id),
      to: `${ride.end_location.street}, ${ride.end_location.postal_code} ${ride.end_location.city}`,
      date: new Date(ride.arrival_time).toLocaleDateString('de-DE', { day: '2-digit', month: 'short' }),
      time: new Date(ride.arrival_time).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' }),
      price: 500 + ' Punkte', // property price does not exist on object that is returned from the db
      image: 'https://randomuser.me/api/portraits/women/1.jpg'
    }))
  } catch {
    showToast('error', 'Fehler beim Abrufen der Fahrten')
  }
}

const filteredRides = computed(() =>
  rides.value.filter((ride) =>
    ride.to.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

onMounted(() => {
  fetchRides()
})
</script>

<template>
  <div class="view-container">
    <div class="map-container" :style="{ height: `${sheetY}px` }">
      <Map />
    </div>

    <BottomSheet v-model="sheetY">
      <SearchBar v-model:query="searchQuery" />
      <div class="fahrten-list">
        <RideCardLaurin v-for="ride in filteredRides" :key="ride.id" :ride="ride" />
      </div>
      <HoverButton :buttons="[{ variant: 'primary', text: 'Logout', color: 'danger', onClick: () => console.log('logout') }]" />
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

.fahrten-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}
</style>
