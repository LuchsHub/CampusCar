import type { CodriveBase } from "./Codrive"
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

// backend representation which is returned via api
export interface RideGet extends Record<string, string | number | LocationGetDto | number[][] | CodriveBase[]>{
  id: string
  driver_id: string
  car_id: string
  max_n_codrives: number | string
  max_request_distance: number | string
  departure_date: string
  departure_time: string
  arrival_time:  string
  arrival_date: string
  start_location: LocationGetDto
  end_location: LocationGetDto
  n_codrives: number
  route_geometry: number[][]
  codrives: CodriveBase[]
  estimated_duration_seconds: number,
  estimated_distance_meters: number
}

export interface RideGetDto extends Record<string, string | number | number[][] | LocationGetDto | boolean | undefined> {
  type: "own" | "booked" | "other" // other = another user posted the ride
  departure_date: string
  departure_time: string
  arrival_time:  string
  start_location: LocationGetDto
  end_location: LocationGetDto
  route_geometry: number[][]
  max_n_codrives: number | string
  state: "default" | "new request" | "accepted" | "not accepted yet" | "rejected" | "payment outstanding"
  point_reward?: number // reward you get when its your own ride (sum of point_contribution for every accepted codrive)
  point_cost?: number // your cost for a booked ride (point_contribution for your codrive)
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