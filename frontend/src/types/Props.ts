export interface ButtonProps {
  variant: 'primary' | 'secondary'
  color: 'primary' | 'danger'
  to?: string
}

export interface InputProps {
  type: 'text' | 'email' | 'password' | 'date' | 'time' | 'number'
  label: string
  placeholder?: string
}