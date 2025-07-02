import type { LocationCreate } from "./Location"

export interface RideCreateBase extends Record<string, string | number>{
    car_id: string
    max_n_codrives: number | string
    max_request_distance: number | string
    arrival_time:  string
    arrival_date: string
}

export interface RideCreateComplete extends Record<string, string | number | LocationCreate>{
    car_id: string
    max_n_codrives: number | string
    max_request_distance: number | string
    arrival_time:  string
    arrival_date: string
    start_location: LocationCreate
    end_location: LocationCreate
}