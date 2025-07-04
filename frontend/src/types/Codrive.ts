import type { LocationGetDto } from "./Location"
import type { UserGet as UserGetDto } from "./User"

export interface CodriveGet extends Record<string, string | boolean | number | UserGetDto | LocationGetDto> {
    accepted: boolean
    point_contribution: number
    arrival_time: string
    arrival_date: string
    user: UserGetDto
    location: LocationGetDto
}