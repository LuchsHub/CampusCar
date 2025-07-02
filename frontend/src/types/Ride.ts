import type { LocationCreate, LocationGet } from "./Location"

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

export interface RideGet extends Record<string, string | number | LocationGet | number[][]>{
    id: string
    driver_id: string
    car_id: string
    max_n_codrives: number | string
    max_request_distance: number | string
    departure_date: string
    departure_time: string
    arrival_time:  string
    arrival_date: string
    start_location: LocationGet
    end_location: LocationGet
    n_codrives: number,
    route_geometry: number[][]
    estimated_duration_seconds: number,
    estimated_distance_meters: number
}