import type { LocationCreateDto } from '@/types/Location';
import { reactive } from 'vue';
import { required, isValidPostalCode } from '@/services/validation';
import type { ValidationSchema } from '@/types/Validation';


export function useLocation() {

  const getEmptyLocationCreate = (): LocationCreateDto => {
    return reactive<LocationCreateDto>({
        country: "Deutschland",
        postal_code: "",
        city: "",
        street: "",
        house_number: "",
    })
  }

  const getLocationCreateValidationSchema = (): ValidationSchema => {
    return {
      country: [required('Land')],
      postal_code: [required('PLZ'), isValidPostalCode()],
      city: [required('Stadt')],
      street: [required('Straße')],
      house_number: [required('Hausnummer')],
    }
  }


  return {
    getEmptyLocationCreate,
    getLocationCreateValidationSchema,
  }
}
