import api from '@/services/api';
import axios from 'axios';
import { useToaster } from '@/composables/useToaster';
import type { EstimatedCostsGet } from '@/types/Codrive';
import type { LocationCreateDto } from '@/types/Location';


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

  const deleteBookedCodrive = async (codriveId: string) => {
    try {
      await api.delete(`codrives/${codriveId}/own`);
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Absagen der Mitfahrt. Versuche es später nochmal.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  const previewCodriveCost = async (rideId: string, location: LocationCreateDto): Promise<number> => {
    const result = await api.post(
      `codrives/${rideId}/preview`,
      {'location': location}
    );
    const data: EstimatedCostsGet = result.data
    return data.point_contribution;
  }

  const payForCodrive = async (codriveId: string, rating: number): Promise<void> => {
    await api.patch(
      `codrives/${codriveId}/pay`,
      {'rating': rating}
    );
  }

  return {
    acceptCodrive,
    rejectCodrive,
    deleteBookedCodrive,
    previewCodriveCost,
    payForCodrive
  }
}
