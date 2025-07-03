<script setup lang="ts">
import Map from '../components/Map.vue'
import SearchBar from '../components/SearchBar.vue'
import HoverButton from '../components/HoverButton.vue'
import BottomSheet from '../components/BottomSheet.vue'
import { ref, computed, onMounted } from 'vue'
import type { RideGetDto } from '../types/Ride' // removed import for RideDto because of linting
import { useRide } from '@/composables/useRide'
import RideCard from '@/components/RideCard.vue'

const { getAllRides } = useRide();
const searchQuery = ref('')
const rides = ref<RideGetDto[]>([])
const sheetY = ref(0)

const filteredRides = computed(() =>
  rides.value.filter((ride) =>
    ride.end_location.city.toLowerCase().includes(searchQuery.value.toLowerCase()) // city for now, other stuff can be added
  )
);

onMounted( async () => {
  rides.value = await getAllRides();
})
</script>

<template>
  <div class="view-container">
    <div class="map-container" :style="{ height: `${sheetY}px` }">
      <Map />
    </div>

    <BottomSheet v-model="sheetY">
      <SearchBar v-model:query="searchQuery" />
      <div class="ride-list">
        <template v-for="(ride, index) in filteredRides" :key="ride.id">
          <RideCard :ride="ride"/>
          <hr v-if="index < filteredRides.length - 1" />
        </template>
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

.ride-list {
  display: flex;
  flex-direction: column;
  margin-top: 1rem;
}
</style>
