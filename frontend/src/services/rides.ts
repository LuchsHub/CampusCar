// src/services/rides.ts
import api from './api'
import type { RideDto } from '@/types/Ride'

export const fetchRidesFromApi = async (): Promise<RideDto[]> => {
  const res = await api.get('/rides/')
  const data = res.data.results || res.data
  if (!Array.isArray(data)) {
    throw new Error('Die API-Antwort ist kein Array.')
  }
  return data
}
