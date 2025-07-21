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
import { useToaster } from '@/composables/useToaster'
import { useUserLocationStore } from '@/stores/UserLocationStore'
import userIconUrl from '@/assets/icons_new/user.svg'
import startDefaultIconUrl from '@/assets/icons_new/start_default.svg'
import startActiveIconUrl from '@/assets/icons_new/start_active.svg'
import goalDefaultIconUrl from '@/assets/icons_new/goal_default.svg'
import goalActiveIconUrl from '@/assets/icons_new/goal_active.svg'
import type { RideGetDto } from '@/types/Ride'

const mapContainer = ref<HTMLElement | null>(null)
let map: L.Map | null = null
const userMarker = ref<L.Marker | null>(null)
let routePolyline: L.Polyline | null = null

const rideMarkers: L.Marker[] = []
const isLoading = ref(true)
const lastClickedRideId = ref<string | null>(null)
const selectedRideIdLocal = ref<string | null>(null)

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
  selectedRideId?: string | null
  bottomSheetHeight?: number
}>()

const emit = defineEmits<{
  // eslint-disable-next-line no-unused-vars
  (e: 'update:selectedRideId', id: string): void
}>()

const userIcon = L.icon({
  iconUrl: userIconUrl,
  iconSize: [32, 32], // ggf. anpassen
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
})

const startDefaultIcon = L.icon({
  iconUrl: startDefaultIconUrl,
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
})

const startActiveIcon = L.icon({
  iconUrl: startActiveIconUrl,
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
})

const goalDefaultIcon = L.icon({
  iconUrl: goalDefaultIconUrl,
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
})

const goalActiveIcon = L.icon({
  iconUrl: goalActiveIconUrl,
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
})

const loadFullRideAndGoToRequest = async (rideId: string) => {
  try {
    const ride = props.rides.find(ride => ride.id === rideId);
    myRideStore.setRide(ride as unknown as RideGetDto);
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
  selectedRideIdLocal.value = ride.id
  emit('update:selectedRideId', ride.id)

  // Zuerst Marker neu rendern (ohne Route)
  renderRides()

  // Dann Route neu setzen
  const latLngs = ride.route_geometry.map(([lng, lat]) => [lat, lng]) as [number, number][]
  if (routePolyline) {
    map.removeLayer(routePolyline)
  }

  routePolyline = L.polyline(latLngs, {
    color: getPrimaryColorActive(),
    weight: 5
  }).addTo(map)

  routePolyline.on('click', () => {
    loadFullRideAndGoToRequest(ride.id)
  })

  map.fitBounds(routePolyline.getBounds(), { padding: [50, 50] })
}

  props.rides.forEach((ride) => {
  const start: L.LatLngExpression = [ride.start_location.latitude, ride.start_location.longitude]
  const end: L.LatLngExpression = [ride.end_location.latitude, ride.end_location.longitude]

  const isSelected = selectedRideIdLocal.value === ride.id

  const startMarker = L.marker(start, { icon: isSelected ? startActiveIcon : startDefaultIcon })
    .addTo(map!)
    .bindPopup('Startpunkt')
    .on('click', () => handleRideClick(ride))

  const endMarker = L.marker(end, { icon: isSelected ? goalActiveIcon : goalDefaultIcon })
    .addTo(map!)
    .bindPopup('Zielpunkt')
    .on('click', () => handleRideClick(ride))

  rideMarkers.push(startMarker, endMarker)
})

}

function getPrimaryColorActive(): string {
  const style = getComputedStyle(document.documentElement)
  return style.getPropertyValue('--color-primary-500')?.trim() || '#3b82f6' // fallback
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
    userMarker.value = L.marker(latlng, { icon: userIcon }).addTo(map).bindPopup('Dein Standort')
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

watch(
  () => props.selectedRideId,
  (newId) => {
    if (!newId || !map) return;

    const ride = props.rides.find(r => r.id === newId);
    if (!ride) return;

    selectedRideIdLocal.value = ride.id; // 👉 wichtig: Marker bekommen die active Icons
    renderRides(); // 👉 Marker neu zeichnen mit den neuen Icons

    const latLngs = ride.route_geometry.map(([lng, lat]) => [lat, lng]) as [number, number][];

    if (routePolyline) {
      map.removeLayer(routePolyline);
    }

    routePolyline = L.polyline(latLngs, {
      color: getPrimaryColorActive(), // 👉 grün
      weight: 5
    }).addTo(map);

    map.fitBounds(routePolyline.getBounds(), {
      paddingTopLeft: [50, 0],
      paddingBottomRight: [50, (props.bottomSheetHeight ?? 300) + 80],
    });
  }
);
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
