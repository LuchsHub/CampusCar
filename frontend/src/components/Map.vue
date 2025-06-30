<template>
  <div id="map" ref="mapContainer"/>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import L from 'leaflet'

const mapContainer = ref<HTMLElement | null>(null)
let map: L.Map | null = null

onMounted(() => {
  if (mapContainer.value && !map) {
    map = L.map(mapContainer.value).setView([52.416, 12.550], 13)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)
  }

  setTimeout(() => {
    map?.invalidateSize()
  }, 200)
})
</script>

<style scoped>
#map {
  width: 100%;
  height: 100%;
  border-radius: 12px;
}
</style>
