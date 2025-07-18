import api from '@/services/api';
import axios from 'axios';
import { useToaster } from '@/composables/useToaster';


export function useCodrive() {
  
  const { showDefaultError, showToast } = useToaster()
  
  const acceptCodrive = async (codriveId: string) => {
    try {
        await api.patch(`codrives/${codriveId}/accept`);
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          showToast('error', 'Fehler beim Akzeptieren der Mitfahrt. Versuche es später nochmal.');
        } else {
          showDefaultError();
        }
        throw error
      }
  }
  
  const rejectCodrive = async (codriveId: string) => {
    try {
        await api.delete(`codrives/${codriveId}/passenger`);
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          showToast('error', 'Fehler beim Ablehnen der Mitfahrt. Versuche es später nochmal.');
        } else {
          showDefaultError();
        }
        throw error
      }
  }

  return {
    acceptCodrive,
    rejectCodrive
  }
}
