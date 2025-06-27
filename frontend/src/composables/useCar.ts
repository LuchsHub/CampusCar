import type { CarCreate } from '@/types/Car';
import { reactive } from 'vue';


export function useCar() {

  const getEmptyCarCreate = (): CarCreate => {
    return reactive<CarCreate>({
      n_seats: 5,
      model: "",
      brand: "",
      color: "",
      license_plate: "string",
    })
  }

  return {
    getEmptyCarCreate,
  }
}
