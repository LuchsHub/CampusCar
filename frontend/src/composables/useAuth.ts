import api from '@/services/api'
import { useAuthStore } from '@/stores/AuthStore';
import type { UserRegister, UserLogin } from '@/types/User';
import axios from 'axios';
import { useToaster } from '@/composables/useToaster';

export function useAuth() {
  const authStore = useAuthStore(); // load AuthStore in the function, other wise you will receive a "no active pinia" error on application startup
  const { showToast, showDefaultError } = useToaster();

  const loginUser = async (user: UserLogin) => {
    try {
      const data = await postLoginData(user)
      authStore.setAccessToken(data.access_token);
    } catch (error: unknown) {
      console.log(error);
    }
  }

  // NOTE: This method does not use the api service since it requires some weird input format, for everything else the api service should be fine
  const postLoginData = async (user: UserLogin) => {
    const data = new URLSearchParams();
    data.append("grant_type", "password");
    data.append("username", user.email); 
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
      showToast('success', 'Anmeldung erfolgreich.');
      return response.data
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          showToast('error', 'Ungültige Anmeldedaten.');
        } else {
          showDefaultError();
        }
        throw error
    }
  }

  const registerUser = async (user: UserRegister): Promise<void> => {
    try {
      await postRegisterData(user);

      // turn UserRegister into UserLogin
      const userLogin: UserLogin = {
        email: user.email,
        password: user.password
      }

      const data = await postLoginData(userLogin);
      authStore.setAccessToken(data.access_token);
    } catch (error: unknown) {
      console.log(error);
      throw error;
    }
  }

  const postRegisterData = async (user: UserRegister) => {
    try {
      const response = await api.post(
        '/users/signup',
        user
      )
      showToast('success', 'Registrierung erfolgreich.');
      return response.data
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          showToast('error', 'Fehler beim Registrierungsprozess. Versuche es später nochmal.');
        } else {
          showDefaultError();
        }
        throw error
  }
  }

  const logoutUser = () => {
    authStore.removeAccessToken();
    showToast('success', "Logout erfolgreich.");
  }

  return {
    registerUser,
    loginUser,
    logoutUser,
  }
}
