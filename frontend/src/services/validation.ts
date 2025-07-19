import type { ValidationRule, ValidationSchema } from "@/types/Validation"

export function validate(values: Record<string, string>, schema: ValidationSchema) {
  const errors: Record<string, string[]> = {}
  for (const field in schema) {
    const rules = schema[field] // functions like required()
    const value = values[field] // field value e.g. name = "Albert"

    const fieldErrors = rules
      .map(rule => rule(value))
      .filter((msg): msg is string => !!msg) // filter null values

    if (fieldErrors.length > 0) {
      errors[field] = fieldErrors
    }
  }
  return errors
}

// TODO: add more reusable rules as higher order functions (function that returns a function) here 
export const required = (fieldName: string): ValidationRule => (value) => {
  if (value === undefined || value === null || value === '') return `${fieldName} ist erforderlich`
  return null
}

export const minLength = (min: number, msg: string): ValidationRule => (value) => {
  if (typeof value === 'string' && value.length < min) return msg
  return null
}

export const isDate = (msg: string = 'Ungültiges Datum'): ValidationRule => (value) => {
  if (!value || isNaN(Date.parse(value))) return msg
  const inputDate = new Date(value)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  if (inputDate < today) return msg
  return null
} 

export const isValidPassword = (msg = 'Passwort muss mind. 8 Zeichen, Groß-/Kleinbuchstaben & 1 Zahl enthalten.'): ValidationRule => (value) => {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
  if (typeof value !== 'string' || !regex.test(value)) return msg
  return null
}

export const isValidEmail = (msg = 'Ungültige E-Mail-Adresse'): ValidationRule => (value) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (typeof value !== 'string' || !regex.test(value)) return msg
  return null
}

export const isTHBEmail = (msg = 'Nur THB-Mailadressen erlaubt'): ValidationRule => (value) => {
  if (typeof value !== 'string' || !value.endsWith('@th-brandenburg.de')) return msg
  return null
}

export const isValidPostalCode = (msg = 'Ungültige Postleitzahl'): ValidationRule => (value) => {
  if (typeof value !== 'string' || !/^\d{5}$/.test(value)) return msg
  return null
}

export const largerThan = (min: number, msg: string): ValidationRule => (value) => {
  const numValue = Number(value)
  if (isNaN(numValue) || numValue <= min) return msg
  return null
}

export const smallerThan = (max: number, msg: string): ValidationRule => (value) => {
  const numValue = Number(value)
  if (isNaN(numValue) || numValue >= max) return msg
  return null
}

export const isValidLicensePlate = (msg = 'Ungültiges KFZ-Kennzeichen'): ValidationRule => (value) => {
  const regex = /^[A-ZÄÖÜ]{1,3}-[A-ZÄÖÜ]{1,2}-\d{1,4}$|^[A-ZÄÖÜ]{1,3}-\d{1,4}$/
  if (typeof value !== 'string' || !regex.test(value.toUpperCase())) return msg
  return null
}

