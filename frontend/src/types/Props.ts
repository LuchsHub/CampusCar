export interface ButtonProps {
  variant: 'primary' | 'secondary'
  color: 'primary' | 'danger'
  to?: string
  text?: string
}

export interface HoverButtonProps {
  buttons: ButtonProps[]
}

export interface InputProps {
  type: 'text' | 'email' | 'password' | 'date' | 'time' | 'number' | 'checkbox'
  label: string
  placeholder?: string
}