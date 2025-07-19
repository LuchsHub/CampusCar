import type { CodriveGetDto, RequestedCodriveGetDto } from "./Codrive"
import type { LocationCreateDto, LocationGetDto } from "./Location"
import type { UserGet } from "./User"

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
export interface RideGet extends Record<string, string | number | LocationGetDto | number[][] | RequestedCodriveGetDto[] | CodriveGetDto[] | UserGet>{
  id: string
  driver: UserGet
  car_id: string
  max_n_codrives: number
  n_codrives: number
  max_request_distance: number | string
  departure_date: string
  departure_time: string
  arrival_time:  string
  arrival_date: string
  start_location: LocationGetDto
  end_location: LocationGetDto
  route_geometry: number[][]
  codrives: CodriveGetDto[]
  requested_codrives: RequestedCodriveGetDto[]
  estimated_duration_seconds: number,
  estimated_distance_meters: number
}

export interface RideGetDto extends Record<string, string | number | number[][] | LocationGetDto | RequestedCodriveGetDto[] | CodriveGetDto[] | boolean | undefined | UserGet> {
  id: string
  codrive_id?: string // to reference booked codrive on a ride. only necessary when type = "booked"
  type: "own" | "booked" | "other" // other = another user posted the ride
  departure_time: string
  departure_date: string
  arrival_time:  string
  arrival_date: string
  start_location: LocationGetDto
  end_location: LocationGetDto
  route_geometry: number[][]
  n_available_seats: number
  codrives: CodriveGetDto[]
  requested_codrives: RequestedCodriveGetDto[]
  state: "default" | "new request" | "accepted" | "not accepted yet" | "rejected" | "payment outstanding"
  max_request_distance?: number
  point_reward?: number // reward you get when its your own ride (sum of point_contribution for every accepted codrive)
  point_cost?: number // your cost for a booked ride (point_contribution for your codrive)
  image?: string // user profile picture
  driver: UserGet
}
