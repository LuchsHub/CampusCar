import type { UserRegister, UserLogin } from '../types/User';
import { reactive } from 'vue';


export function useUser() {

  const getEmptyLoginUser = (): UserLogin => {
    return reactive<UserLogin>({
        email: "",
        password: "",
    })
  }
  
  const getEmptyRegisterUser = (): UserRegister => {
    return reactive<UserRegister>({
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        user_name: "",
    })
  }

  return {
    getEmptyLoginUser,
    getEmptyRegisterUser
  }
}
