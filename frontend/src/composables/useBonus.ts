import type { BonusGet } from '@/types/Bonus';
import { useToaster } from './useToaster';
const { showToast } = useToaster()
import api from '@/services/api';


export function useBonus() {

  const getAllBonuses = async (): Promise<BonusGet[]> => {
    try {
      const result = await api.get('/bonuses/');
      return result.data;
    } catch (error: unknown) {
      showToast('error', 'Fehler beim Abrufen der Prämien.');
      console.log(error);
      return []
    }
  }
  
  const getUsersBonuses = async (): Promise<BonusGet[]> => {
    try {
      const result = await api.get('/bonuses/me');
      return result.data;
    } catch (error: unknown) {
      showToast('error', 'Fehler beim Abrufen deiner Prämien.');
      console.log(error);
      return []
    }
  }
  
  const redeemBonus = async (bonusId: string): Promise<void> => {
      await api.post(`/bonuses/redeem/${bonusId}`);
  }

  return {
    getAllBonuses,
    getUsersBonuses,
    redeemBonus
  }
}
