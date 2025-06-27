export interface LocationCreate extends Record<string, string | number>{
    country: string;
    postal_code: string;
    city: string;
    street: string;
    house_number: string;
  }