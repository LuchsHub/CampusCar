export type ValidationRule = (value: any, allValues?: Record<string, any>) => string | null

export type ValidationSchema = {
  [field: string]: ValidationRule[]
}

export function validate(values: Record<string, any>, schema: ValidationSchema) {
  const errors: Record<string, string[]> = {}
  for (const field in schema) {
    const rules = schema[field]
    const value = values[field]
    const fieldErrors = rules
      .map(rule => rule(value, values))
      .filter((msg): msg is string => !!msg)
    if (fieldErrors.length > 0) {
      errors[field] = fieldErrors
    }
  }
  return errors
}

// TODO: add more reusable rules here 
export const required = (msg = 'Required'): ValidationRule => (value) => {
  if (value === undefined || value === null || value === '') return msg
  return null
}

export const minLength = (min: number, msg?: string): ValidationRule => (value) => {
  if (typeof value === 'string' && value.length < min) return msg || `Must be at least ${min} characters`
  return null
}

export const isDate = (msg = 'Invalid date'): ValidationRule => (value) => {
  if (!value || isNaN(Date.parse(value))) return msg
  return null
} 