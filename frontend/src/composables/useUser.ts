import type { UserRegister, UserLogin, UserUpdate } from '@/types/User';
import { reactive } from 'vue';
import { useLocation } from './useLocation';
import api from '@/services/api';
import axios from 'axios';
import { useAuthStore } from '@/stores/AuthStore';

const { getEmptyLocationCreate } = useLocation()
const authStore = useAuthStore()


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


  const updateUser = async (user: UserUpdate) => {
    await postUpdateUserData(user);

    // turn UserRegister into UserLogin
    const userLogin: UserLogin = {
      email: user.email,
      password: user.password
    }

    const data = await postLoginData(userLogin);
    authStore.setAccessToken(data.access_token);
    router.push('/signup/address');
}

const postUpdateUserData = async (user: UserUpdate) => {
  try {
    const response = await api.patch(
      '/users/me',
      user
    )
    return response.data
  } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        console.error('Axios Error:', error.response?.data || error.message)
      } else {
        console.error('Unbekannter Fehler:', error)
      }
      throw error
  }
}

  return {
    getEmptyUserLogin,
    getEmptyUserRegister,
    getEmptyUserUpdate
  }
}
