import api from '@/services/api'
import { useAuth } from '@/composables/useAuth'
import { useToaster } from '@/composables/useToaster'

export function useAccount() {
  const auth = useAuth()
  const { showToast } = useToaster()

  const deleteAccount = async () => {
    try {
      const res = await api.delete('/users/me')
      console.log('Konto erfolgreich gelöscht:', res.data)
      auth.logoutUser()
    } catch (error) {
      const message =
        (error as any)?.response?.data?.message ||
        (error as any)?.message ||
        'Unbekannter Fehler'
      console.error('Fehler beim Löschen:', message)
      showToast('error', message)
    }
  }

  return { deleteAccount }
}
