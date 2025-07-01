export interface RideCreate extends Record<string, string | number>{
    car_id: number | string
    max_n_codrives: number
    max_request_distance: number
    time_of_arrival: number | string
}