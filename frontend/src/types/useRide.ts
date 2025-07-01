import { reactive } from 'vue';
import type { RideCreate } from './Ride';

export function useRide() {

  const getEmptyRideCreate = (): RideCreate => {
    return reactive<RideCreate>({
        car_id: "",
        max_n_codrives: 0,
        max_request_distance: 0,
        time_of_arrival: "",
    })
  }


  return {
    getEmptyRideCreate,
  }
}
