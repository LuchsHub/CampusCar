import api from '@/services/api'
import { useAuth } from '@/composables/useAuth'
import { useToaster } from '@/composables/useToaster'

export function useAccount() {
  const auth = useAuth()
  const { showToast } = useToaster()

  const deleteAccount = async () => {
    try {
      await api.delete('/users/me')
      auth.logoutUser()
    } catch {
      showToast('error', 'Fehler beim Löschen des Kontos')
    }
  }

  return { deleteAccount }
}
