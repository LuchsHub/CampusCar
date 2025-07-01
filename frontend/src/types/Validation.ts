export type ValidationRule = (_value: string, _allValues?: Record<string, string>) => string | null

// Validationschema keys have to be the same as in the object you want to validate
// e.g. ride = {date: "", departureTime: "", ...} -> rideValidationSchema = {date: rule(), departureTime: rule(), ...}
export type ValidationSchema = Record<string, ValidationRule[]>