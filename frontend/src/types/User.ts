interface BaseUser {
    email: string
    password: string
  }
  
export interface UserLogin extends BaseUser {}

export interface UserRegister extends BaseUser {
  first_name: string
  last_name: string
  user_name: string
}