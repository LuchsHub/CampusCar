import type { LocationCreate } from "./Location"

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