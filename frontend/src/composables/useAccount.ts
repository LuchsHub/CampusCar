import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/AuthStore'
import api from '@/services/api'

export function useAccount() {
  const router = useRouter()
  const authStore = useAuthStore()

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

      authStore.removeAccessToken()
      router.push('/login')
    } catch (error) {
      console.error('Fehler beim Löschen des Kontos:', error)
      alert('❌ Konto konnte nicht gelöscht werden.')
    }
  }

  return { deleteAccount }
}
