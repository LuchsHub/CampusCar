import type { UserRegister, UserLogin, UserUpdate, UserGet } from '@/types/User';
import type { LocationCreateDto, LocationGetDto } from '@/types/Location';
import { reactive } from 'vue';
import { useLocation } from './useLocation';
import api from '@/services/api';
import axios from 'axios';
import { useToaster } from './useToaster';
import profilePicturePlaceholder from '@/assets/profile_picture_placeholder.svg';

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

  const checkUserHasLicense = async (): Promise<boolean> => {
    const user: UserGet = await getUserMe();
    return user.has_license
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

  const uploadProfileImage = async (file: File): Promise<void> => {
    const formData = new FormData()
    formData.append('profile_picture', file)
    
    await api.put('/users/me/img', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  const getProfileImageUrl = async (userId: string): Promise<string | null> => {
    try {
      const response = await api.get(`/users/${userId}/img`, {
        responseType: 'blob',
        headers: {
          Accept: 'image/*'
        }
      })

      const contentType = response.headers['content-type']
      if (response.status === 200 && contentType?.startsWith('image')) {
        return URL.createObjectURL(response.data);
      } else {
        return profilePicturePlaceholder;
      }
    } catch (error) {
      console.warn('Profilbild konnte nicht geladen werden', error)
      return profilePicturePlaceholder
    }
  }

  const getUserBalance = async (): Promise<number> => {
    try {
      const user = await getUserMe();
      return user.cash;
    } catch (error: unknown) {
      showToast('error', 'Fehler beim Abrufen des Guthabens.');
      console.log(error);
      return 0
    }
  }

  const chargeUserBalance = async (charges: number): Promise<number> => {
    try {
      const result = await api.post(`users/charge?charges=${charges}`);
      const user: UserGet = result.data
      return user.cash;
    } catch (error: unknown) {
      showDefaultError();
      throw error;
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
    postUpdateUserData,
    uploadProfileImage,
    getProfileImageUrl,
    checkUserHasLicense,
    getUserBalance,
    chargeUserBalance
  }
}
