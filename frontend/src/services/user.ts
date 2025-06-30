// services/user.ts
import axios from 'axios'

export interface CurrentUser {
  id: number
  user_name: string
  first_name: string
  last_name: string
  email: string
  avatar_url?: string
}

export const fetchCurrentUser = async (): Promise<CurrentUser> => {
  const response = await axios.get('/api/v1/users/me')
  return response.data
}