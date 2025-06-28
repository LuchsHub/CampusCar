export interface PageTitleProps {
  to?: string
}
export interface ButtonProps {
  variant: 'primary' | 'secondary' | 'tertiary'
  color?: 'danger'
  to?: string 
  text?: string
  onClick?: () => void
}

export interface HoverButtonProps {
  buttons: ButtonProps[]
}

export interface InputProps {
  modelValue: string | number
  type: 'text' | 'email' | 'password' | 'date' | 'time' | 'number' | 'checkbox' | 'file'
  label: string
  placeholder?: string
  maxLength?: number
}