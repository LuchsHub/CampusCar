import type { UserRegister, UserLogin, UserUpdate } from '@/types/User';
import type { LocationCreate } from '@/types/Location';
import { reactive } from 'vue';
import { useLocation } from './useLocation';
import api from '@/services/api';

const { getEmptyLocationCreate } = useLocation()


export function useUser() {

  const getEmptyUserLogin = (): UserLogin => {
    return reactive<UserLogin>({
        email: "",
        password: "",
    })
  }
  
  const getEmptyUserRegister = (): UserRegister => {
    return reactive<UserRegister>({
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        user_name: "",
    })
  }
  
  const getEmptyUserUpdate = (): UserUpdate => {
    return reactive<UserUpdate>({
      first_name: "",
      last_name: "",
      user_name: "",
      email: "",
      location: getEmptyLocationCreate()
    })
  }


  // functions 
  const updateUserLocation = async (location: LocationCreate) => {
    // wrap location in a UserUpdate object
    const userUpdateWithLocation = {
      location: location
    }
    await postUpdateUserData(userUpdateWithLocation)
  }

  const postUpdateUserData = async (user: UserUpdate) => {
    try {
      const response = await api.patch(
        '/users/me',
        user
      )
      return response.data
    } catch (error: unknown) {
        throw error
    }
  }

  return {
    getEmptyUserLogin,
    getEmptyUserRegister,
    getEmptyUserUpdate,
    updateUserLocation
  }
}
