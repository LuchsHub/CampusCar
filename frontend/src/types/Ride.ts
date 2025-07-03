import type { LocationCreateDto, LocationGetDto } from "./Location"

export interface RideCreateBase extends Record<string, string | number>{
    car_id: string
    max_n_codrives: number | string
    max_request_distance: number | string
    arrival_time:  string
    arrival_date: string
}

export interface RideCreateComplete extends Record<string, string | number | LocationCreateDto>{
    car_id: string
    max_n_codrives: number | string
    max_request_distance: number | string
    arrival_time:  string
    arrival_date: string
    start_location: LocationCreateDto
    end_location: LocationCreateDto
}

export interface RideGetDto extends Record<string, string | number | number[][] | LocationGetDto | boolean> {
  type: "own" | "booked" | "other" // other = another user posted the ride
  departure_date: string
  departure_time: string
  arrival_time:  string
  start_location: LocationGetDto
  end_location: LocationGetDto
  route_geometry: number[][]
  max_n_codrives: number | string
  state: "default" | "new request" | "accepted" | "not accepted yet" | "rejected" | "payment outstanding"
}

// export interface RideCardData {
//   id: number
//   to: string
//   date: string
//   time: string
//   price: string
//   image: string
// }

// export interface RideDto {
//   id: number
//   arrival_time: string
//   price: number
//   end_location: {
//     street: string
//     postal_code: string
//     city: string
//   }
// }