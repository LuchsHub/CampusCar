export interface LocationCreate extends Record<string, string | number>{
  country: string;
  postal_code: number | string;
  city: string;
  street: string;
  house_number: string;
}

export interface LocationGet extends Record<string, string | number | undefined>{
  id: string
  country: string;
  postal_code: number | string;
  city: string;
  street: string;
  house_number: string;
  latitude: number
  longitude: number
}