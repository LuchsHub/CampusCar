import type { LocationCreateDto, LocationGetDto } from "./Location"

export interface UserLogin extends Record<string, string>  {
  email: string
  password: string
}

export interface UserRegister extends Record<string, string>  {
  user_name: string
  first_name: string
  last_name: string
  email: string
  password: string
}

export interface UserUpdate extends Record<string, string | boolean | LocationCreateDto | undefined>  {
  user_name?: string
  first_name?: string
  last_name?: string
  email?: string
  location?: LocationCreateDto 
  has_license?: boolean
}

export interface UserGet extends Record<string, string | boolean | LocationGetDto | null> {
  id: string
  email: string
  is_active: boolean
  is_superuser: boolean
  first_name: string
  last_name: string
  user_name: string
  has_license: boolean
  location: LocationGetDto | null
}

export interface CurrentUser {
  id: number
  user_name: string
  first_name: string
  last_name: string
  email: string
  avatar_url?: string
  rating: number
}