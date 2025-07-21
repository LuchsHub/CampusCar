import { defineStore } from 'pinia'

export const useUserLocationStore = defineStore('userLocation', {
  state: () => ({
    coords: null as [number, number] | null,
    loading: false,
    error: null as string | null
  }),
  actions: {
    async fetchLocation() {
      if (this.coords) return // bereits geladen ✅

      this.loading = true
      this.error = null

      try {
        const position = await new Promise<GeolocationPosition>((resolve, reject) =>
          navigator.geolocation.getCurrentPosition(resolve, reject)
        )
        this.coords = [position.coords.latitude, position.coords.longitude]
      } catch {
        this.error = 'Standort konnte nicht ermittelt werden'
      } finally {
        this.loading = false
      }
    }
  }
})
