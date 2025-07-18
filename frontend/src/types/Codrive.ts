import type { LocationGetDto } from "./Location"
import type { RideGet } from "./Ride"
import type { UserGet, UserGet as UserGetDto } from "./User"

export interface MyCodriveGet extends Record<string, string | number | boolean | RideGet> {
    id: string
    point_contribution: number
    accepted: boolean
    paid: boolean
    ride: RideGet
}

export interface CodriveGetDto extends Record<string, string | boolean | number | UserGetDto | LocationGetDto> {
    id: string
    arrival_time: string
    arrival_date: string
    user: UserGetDto
    location: LocationGetDto
    point_contribution: number
    n_passengers: number
}

export interface RequestedCodriveGetDto extends Record<string, string | boolean | number | UserGetDto | LocationGetDto | RouteUpdateGet> {
    id: string
    accepted: boolean
    arrival_time: string
    arrival_date: string
    user: UserGetDto
    location: LocationGetDto
    route_update: RouteUpdateGet
    point_contribution: number
    n_passengers: number
    message: string
}

export interface RouteUpdateGet extends Record<string, string | CodriverArrivalTimeGet[]> {
    codriver_arrival_times: CodriverArrivalTimeGet[]
    updated_ride_departure_date: string
    updated_ride_departure_time: string
}

export interface CodriverArrivalTimeGet extends Record<string, string | UserGet | LocationGetDto> {
    user: UserGet
    location: LocationGetDto
    arrival_date: string
    arrival_time: string
}

export interface RequestedCodriveDto extends Record<string, string | number | RouteUpdateDto[]> {
    id: string
    first_name: string
    last_name: string
    route_update: RouteUpdateDto[]
    new_departure_date: string
    new_departure_time: string
    point_contribution: number
    n_passengers: number
    message: string
}

export interface RouteUpdateDto extends Record<string, string | LocationGetDto> {
    location: LocationGetDto
    passenger_first_name: string
    passenger_last_name: string
    arrival_date: string
    arrival_time: string
}

