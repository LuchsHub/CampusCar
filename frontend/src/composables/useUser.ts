import type { UserRegister, UserLogin, UserUpdate, UserGet } from '@/types/User';
import type { LocationCreateDto, LocationGetDto } from '@/types/Location';
import { reactive } from 'vue';
import { useLocation } from './useLocation';
import api from '@/services/api';
import axios from 'axios';
import { useToaster } from './useToaster';

const { getEmptyLocationCreate } = useLocation()
const { showDefaultError, showToast } = useToaster()


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
  const updateUserLocation = async (location: LocationCreateDto) => {
    // wrap location in a UserUpdate object
    const userUpdateWithLocation: UserUpdate = {
      location: location
    }
    try {
      await postUpdateUserData(userUpdateWithLocation)
    } catch (error: unknown) {
      console.log(error);
    }
  }

  const updateUserHasLicense = async (has_license: boolean) => {
    const userUpdateWithLicense: UserUpdate = {
      has_license: has_license
    }
    try {
      await postUpdateUserData(userUpdateWithLicense)
    } catch (error: unknown) {
      console.log(error);
    }
  }

  const postUpdateUserData = async (user: UserUpdate) => {
    try {
      const response = await api.patch(
        '/users/me',
        user
      )
      showToast('success', 'Aktualisierung deiner Daten erfolgreich.');
      return response.data
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Aktualisierung der Daten fehlgeschlagen. Versuche es später nochmal.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  const getCurrentUserLocation = async (): Promise<LocationGetDto | null> => {
    try {
      const user: UserGet = await getUserMe();
      return user.location;
    } catch (error: unknown) {
      console.log(error);
      return null
    }
  }

  const getCurrentUserId = async (): Promise<string | null> => {
    try {
      const user: UserGet = await getUserMe();
      return user.id;
    } catch (error: unknown) {
      console.log(error);
      return null
    }
  }

  const getUserMe = async (): Promise<UserGet> => {
    try {
      const response = await api.get(
        '/users/me'
      )
      return response.data
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Abrufen des aktuellen Users.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  return {
    getEmptyUserLogin,
    getEmptyUserRegister,
    getEmptyUserUpdate,
    updateUserLocation,
    updateUserHasLicense,
    getCurrentUserLocation,
    getCurrentUserId,
    getUserMe,
    postUpdateUserData
  }
}
