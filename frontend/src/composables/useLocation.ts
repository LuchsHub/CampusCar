import type { LocationCreate } from '@/types/Location';
import { reactive } from 'vue';


export function useLocation() {

  const getEmptyLocationCreate = (): LocationCreate => {
    return reactive<LocationCreate>({
        country: "",
        postal_code: "",
        city: "",
        street: "",
        house_number: "",
    })
  }


  return {
    getEmptyLocationCreate,
  }
}
