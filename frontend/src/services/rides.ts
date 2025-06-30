// src/services/rides.ts
import api from './api'

export interface RideDto {
  id: number
  arrival_time: string
  price: number
  end_location: {
    street: string
    postal_code: string
    city: string
  }
}

export const fetchRidesFromApi = async (): Promise<RideDto[]> => {
  const res = await api.get('/rides/')
  const data = res.data.results || res.data

  if (!Array.isArray(data)) {
    throw new Error('Die API-Antwort ist kein Array.')
  }

  return data
}
