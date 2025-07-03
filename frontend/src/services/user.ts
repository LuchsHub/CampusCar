// services/user.ts
import api from './api'
import type { CurrentUser } from '@/types/User'

export const fetchCurrentUser = async (): Promise<CurrentUser> => {
  const response = await api.get('users/me')
  return response.data
}