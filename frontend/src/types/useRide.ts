import { reactive } from 'vue';
import type { RideCreateBase, RideGet } from './Ride';
import type { RideCreateComplete } from './Ride';
import api from '@/services/api';
import axios from 'axios';
import { useToaster } from '@/composables/useToaster';
import type { LocationCreate } from './Location';


export function useRide() {
  
  const { showDefaultError, showToast } = useToaster()

  const getEmptyRideCreate = (): RideCreateBase => {
    return reactive<RideCreateBase>({
        car_id: "",
        max_n_codrives: 0,
        max_request_distance: 0,
        arrival_time: "",
        arrival_date: "",
    })
  }

  const postRide = async (ride: RideCreateBase, startLocation: LocationCreate, endLocation: LocationCreate) => {
    const rideComplete: RideCreateComplete = {
      "car_id": ride.car_id,
      "max_n_codrives": ride.max_n_codrives,
      "max_request_distance": ride.max_request_distance,
      "arrival_time": ride.arrival_time,
      "arrival_date": ride.arrival_date,
      "start_location": startLocation,
      "end_location": endLocation,
    }

    await postRideData(rideComplete);
  }

  const postRideData = async (ride: RideCreateComplete): Promise<void> => {
    try {
      await api.post(
        '/rides',
        ride
      );
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim erstellen der Fahrt.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  const getRidesForUser = async (user_id: string): Promise<RideGet[]> => {
    try {
      const result = await api.get(
        `/rides/${user_id}`
      );
      return result.data;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Abrufen deiner Fahrten.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }


  return {
    getEmptyRideCreate,
    postRide,
    getRidesForUser
  }
}
