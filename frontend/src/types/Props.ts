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
  modelValue: string
  type: 'text' | 'email' | 'password' | 'date' | 'time' | 'number' | 'checkbox'
  label: string
  placeholder?: string
}