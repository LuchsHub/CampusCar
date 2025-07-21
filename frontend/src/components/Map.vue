<template>
  <div v-show="isLoading" class="loading-screen">
    <p>Standort wird geladen...</p>
  </div>
  <div v-show="!isLoading" id="map" ref="mapContainer" />
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import { useMyRideStore } from '@/stores/MyRideStore'
import api from '@/services/api'
import { useToaster } from '@/composables/useToaster'
import { useUserLocationStore } from '@/stores/UserLocationStore'

const mapContainer = ref<HTMLElement | null>(null)
let map: L.Map | null = null
let userMarker: L.Marker | null = null
let routePolyline: L.Polyline | null = null

const rideMarkers: L.Marker[] = []
const isLoading = ref(true)
const lastClickedRideId = ref<string | null>(null)

const myRideStore = useMyRideStore()
const router = useRouter()
const { showToast } = useToaster()
const userLocationStore = useUserLocationStore()

const props = defineProps<{
  rides: Array<{
    id: string
    start_location: { latitude: number; longitude: number }
    end_location: { latitude: number; longitude: number }
    route_geometry: number[][]
  }>
}>()

const loadFullRideAndGoToRequest = async (rideId: string) => {
  try {
    const response = await api.get(`/rides/${rideId}`)
    myRideStore.setRide(response.data)
    router.push({ name: 'RideRequest' })
  } catch {
    showToast('error', 'Fehler beim Laden der Fahrt')
  }
}

function renderRides() {
  if (!map) return

  rideMarkers.forEach(marker => map!.removeLayer(marker))
  rideMarkers.length = 0

  if (routePolyline) {
    map.removeLayer(routePolyline)
    routePolyline = null
  }

  const handleRideClick = (ride: typeof props.rides[number]) => {
    if (!map) return

    if (String(lastClickedRideId.value) === String(ride.id)) {
      loadFullRideAndGoToRequest(ride.id)
      return
    }

    lastClickedRideId.value = ride.id

    const latLngs = ride.route_geometry.map(([lng, lat]) => [lat, lng]) as [number, number][]
    if (routePolyline) {
      map.removeLayer(routePolyline)
    }

    routePolyline = L.polyline(latLngs, { color: 'blue', weight: 5 }).addTo(map)

    routePolyline.on('click', () => {
      loadFullRideAndGoToRequest(ride.id)
    })

    map.fitBounds(routePolyline.getBounds(), { padding: [50, 50] })
  }

  props.rides.forEach((ride) => {
    const start: L.LatLngExpression = [ride.start_location.latitude, ride.start_location.longitude]
    const end: L.LatLngExpression = [ride.end_location.latitude, ride.end_location.longitude]

    const startMarker = L.marker(start).addTo(map!).bindPopup('Startpunkt').on('click', () => handleRideClick(ride))
    const endMarker = L.marker(end).addTo(map!).bindPopup('Zielpunkt').on('click', () => handleRideClick(ride))

    rideMarkers.push(startMarker, endMarker)
  })
}

// 📍 Nutzerstandort ermitteln und Karte initialisieren
onMounted(async () => {
  await userLocationStore.fetchLocation()
  const latlng = userLocationStore.coords

  if (!latlng) {
    isLoading.value = false
    return
  }

  isLoading.value = false
  await nextTick()

  if (mapContainer.value && !map) {
    map = L.map(mapContainer.value)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)
  }

  if (map) {
    userMarker = L.marker(latlng).addTo(map).bindPopup('Dein Standort')
    map.setView(latlng, 13)
    setTimeout(() => map?.invalidateSize(), 100)
    renderRides()
  }
})

watch(
  () => props.rides,
  () => {
    renderRides()
  }
)
</script>

<style scoped>
html,
body,
#app {
  height: 100%;
  margin: 0;
}

#map {
  width: 100%;
  height: 100vh;
  border-radius: 12px;
}

.loading-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 1.2rem;
  font-weight: bold;
  background-color: #f5f5f5;
}
</style>
