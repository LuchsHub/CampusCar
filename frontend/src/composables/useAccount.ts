import api from '@/services/api'
import { useAuth } from '@/composables/useAuth';

export function useAccount() {

  const auth = useAuth()

  const deleteAccount = async () => {
    const confirmation = window.prompt(
      '⚠️ Bist du sicher, dass du dein Konto löschen möchtest?\n\nGib bitte "löschen" ein, um fortzufahren.'
    )

    if (confirmation !== 'löschen') {
      alert('Konto wurde nicht gelöscht.')
      return
    }

    try {
      await api.delete('/users/me')

      auth.logoutUser()
    } catch (error) {
      console.error('Fehler beim Löschen des Kontos:', error)
      alert('❌ Konto konnte nicht gelöscht werden.')
    }
  }

  return { deleteAccount }
}
