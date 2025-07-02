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

export interface UserUpdate extends Record<string, string | LocationCreate | undefined>  {
  user_name?: string
  first_name?: string
  last_name?: string
  email?: string
  location?: LocationCreate 
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