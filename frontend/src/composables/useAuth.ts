import api from '../services/api'
import { useAuthStore } from '../stores/AuthStore';
import type { UserRegister, UserLogin } from '../types/User';
import router from "../router";
import axios from 'axios';
import { useToaster } from './useToaster';

const authStore = useAuthStore();
const { showToast } = useToaster();

export function useAuth() {

  const loginUser = async (user: UserLogin) => {
    const data = await postLoginData(user)
    console.log(data);
    authStore.setAccessToken(data.access_token);
    showToast('success', "Anmeldung erfolgreich!")
    router.push('/'); // Navigate to home page
  }

  const postLoginData = async (user: UserLogin) => {
    const data = new URLSearchParams();
    data.append("grant_type", "password");
    data.append("username", user.email); // beachte die URL-kodierte Form
    data.append("password", user.password);
    data.append("scope", "");
    data.append("client_id", "string");
    data.append("client_secret", "string");

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/login/access-token`, data, {
        headers: {
          accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
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

  const registerUser = async (user: UserRegister) => {
      await postRegisterData(user);

      // turn UserRegister into UserLogin
      const userLogin: UserLogin = {
        email: user.email,
        password: user.password
      }

      const data = await postLoginData(userLogin);
      authStore.setAccessToken(data.access_token);
      showToast('success', "Registrierung erfolgreich!")
      router.push('/'); // Navigate to home page
  }

  const postRegisterData = async (user: UserRegister) => {
    try {
      const response = await api.post(
        '/users/signup',
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

  const logoutUser = () => {
    authStore.removeAccessToken();
    showToast('success', "Logout erfolgreich!")
    router.push('/login');
  }

  return {
    registerUser,
    loginUser,
    logoutUser,
  }
}
