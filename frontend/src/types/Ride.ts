// src/types/Ride.ts
export interface RideCardData {
  id: number
  to: string
  date: string
  time: string
  price: string
  image: string
}

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