interface BaseUser {
    email: string
    password: string
  }
  
export interface UserLogin extends BaseUser {}

export interface UserRegister extends BaseUser {
  full_name: string
}