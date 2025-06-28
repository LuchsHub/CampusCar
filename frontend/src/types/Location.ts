export interface LocationCreate extends Record<string, string | number>{
    country: string;
    postal_code: number | string;
    city: string;
    street: string;
    house_number: string;
  }