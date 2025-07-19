import type { CarGet } from "./Car"
import type { CodriveGetDto, RequestedCodriveGetDto } from "./Codrive"
import type { LocationGetDto } from "./Location"
import type { RideGetDto } from "./Ride"

export interface PageTitleProps {
  goBack?: boolean
}
export interface ButtonProps {
  variant: 'primary' | 'secondary' | 'tertiary'
  disabled?: boolean
  color?: 'danger'
  to?: string 
  text?: string
  onClick?: () => void
  loading?: boolean;
}

export interface HoverButtonProps {
  buttons: ButtonProps[]
}

export interface InputProps {
  modelValue: string | number
  type: 'text' | 'email' | 'password' | 'date' | 'time' | 'number' | 'checkbox' | 'file'
  label: string
  placeholder?: string
  maxLength?: number
}

export interface CarSelectProps {
  car: CarGet
  selected: boolean
}

export interface TabSwitcherProps {
  tabs: string[]
  modelValue: string
}

export interface RideCardProps {
  ride: RideGetDto
}

export interface LocationItemProps {
  location: LocationGetDto
  arrival_time: string
  arrival_date?: string
  updated_arrival_time?: string
  user?: {
    first_name: string
    last_name: string
    id?: string
  }
}

export interface CodriveCardProps { 
  codrive?: CodriveGetDto
  requested_codrive?: RequestedCodriveGetDto
  seat_no?: number
}

export interface InformationItemProps {
  type: "availableSeats" | "bookedSeats" | "pointReward" | "pointCost" | "message"
  value: string | number | undefined
}

export interface ProfileCardProps {
  profile_picture: string | undefined
  first_name: string
  last_name: string
  avg_rating: number
}