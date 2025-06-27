export interface CarCreate extends Record<string, string | number> {
  n_seats: number;
  model: string;
  brand: string;
  color: string;
  license_plate: string;
}

export interface CarUpdate extends Record<string, string | number | undefined>{
  n_seats?: number;
  model?: string;
  brand?: string;
  color?: string;
  license_plate?: string;
}
