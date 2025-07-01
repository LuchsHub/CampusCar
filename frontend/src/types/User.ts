import type { LocationCreate, LocationGet } from "./Location"

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

export interface UserUpdate extends Record<string, string | boolean | LocationCreate | undefined>  {
  user_name?: string
  first_name?: string
  last_name?: string
  email?: string
  location?: LocationCreate 
  has_license?: boolean
}

export interface UserMeGet extends Record<string, string | boolean | LocationGet> {
  id: string
  email: string
  is_active: boolean
  is_superuser: boolean
  first_name: string
  last_name: string
  user_name: string
  has_license: boolean
  location: LocationGet
}