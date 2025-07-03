import type { CarGet } from "./Car"
import type { RideGetDto } from "./Ride"

export interface PageTitleProps {
  goBack?: boolean
}
export interface ButtonProps {
  variant: 'primary' | 'secondary' | 'tertiary'
  color?: 'danger'
  to?: string 
  text?: string
  onClick?: () => void
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