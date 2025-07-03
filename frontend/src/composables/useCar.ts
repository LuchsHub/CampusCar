import type { CarCreate, CarGet } from '@/types/Car';
import { reactive } from 'vue';
import api from '@/services/api';
import axios from 'axios';
import { useToaster } from './useToaster';

const { showToast, showDefaultError } = useToaster();

export function useCar() {

  const getEmptyCarCreate = (): CarCreate => {
    return reactive<CarCreate>({
      brand: "",
      model: "",
      n_seats: "",
      color: "",
      license_plate: "",
    })
  }

  const createCar = async (car: CarCreate): Promise<void> => {
    try {
      postCreateCarData(car);
      showToast('success', 'Auto erfolgreich hinzugefügt.');
    } catch (error: unknown) {
      console.log(error);
    }
  }

  const postCreateCarData = async (car: CarCreate) => {
    try {
      const data = api.post(
        '/cars',
        car
      );
      return data;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim hinzufügen des Autos. Versuche es später nochmal.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  const getUserCarsData = async (): Promise<CarGet[]> => {
    try {
      const response = await api.get(
        '/cars'
      )
      return response.data;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Abrufen deiner Autos.');
      } else {
        showDefaultError();
      }
      return [];
    }
  }

  return {
    getEmptyCarCreate,
    createCar,
    getUserCarsData
  }
}
