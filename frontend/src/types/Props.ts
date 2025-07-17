import type { CarGet } from "./Car"
import type { CodriveGetDto } from "./Codrive"
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
  user?: {
    first_name: string
    last_name: string
  }
}

// TODO: maybe you can make the attributes a bit more fine-grained. I dont think we need every attribute of Codrive
export interface CodriveCardProps { 
  codrive_accepted: boolean
  codrive: CodriveGetDto
  seat_no?: number
}