import { reactive } from 'vue';
import type { RideCreateBase, RideGet, RideGetDto } from '../types/Ride';
import type { RideCreateComplete } from '../types/Ride';
import api from '@/services/api';
import axios from 'axios';
import { useToaster } from '@/composables/useToaster';
import type { LocationCreateDto } from '../types/Location';
import type { CodriveBase } from '@/types/Codrive';


export function useRide() {
  
  const { showDefaultError, showToast } = useToaster()

  const getEmptyRideCreate = (): RideCreateBase => {
    return reactive<RideCreateBase>({
        car_id: "",
        max_n_codrives: 0,
        max_request_distance: 0,
        arrival_time: "",
        arrival_date: "",
    })
  }

  const postRide = async (ride: RideCreateBase, startLocation: LocationCreateDto, endLocation: LocationCreateDto) => {
    const rideComplete: RideCreateComplete = {
      "car_id": ride.car_id,
      "max_n_codrives": ride.max_n_codrives,
      "max_request_distance": ride.max_request_distance,
      "arrival_time": ride.arrival_time,
      "arrival_date": ride.arrival_date,
      "start_location": startLocation,
      "end_location": endLocation,
    }

    await postRideData(rideComplete);
  }

  const postRideData = async (ride: RideCreateComplete): Promise<void> => {
    try {
      await api.post(
        '/rides',
        ride
      );
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim erstellen der Fahrt.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  const getRidesForUser = async (user_id: string): Promise<RideGetDto[]> => {
    try {
      const result = await api.get(`/rides/by_driver/${user_id}`);

      if (result.data.data.length === 0) { // idk why it is result.data.data but otherwise it wont work
        return []
      }

      const rideGetDtos: RideGetDto[] = result.data.data.map((ride: RideGet) => ({
        id: ride.id,
        type: "own",
        departure_date: ride.departure_date,
        departure_time: ride.departure_time,
        arrival_time: ride.arrival_time,
        start_location: ride.start_location,
        end_location: ride.end_location,
        route_geometry: ride.route_geometry,
        n_available_seats: ride.max_n_codrives - ride.n_codrives,
        state: ride.codrives.some((codrive: CodriveBase) => codrive.accepted === false) ? "new request" : "default",
        point_reward: ride.requested_codrives
          .filter((codrive: CodriveBase) => codrive.accepted)
          .reduce((sum: number, codrive: CodriveBase) => sum + codrive.point_contribution, 0)
      } as RideGetDto));
      return rideGetDtos;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Abrufen deiner Fahrten.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  const getAllRides = async (): Promise<RideGetDto[]> => {
    try {
      const result = await api.get(`/rides`);

      if (result.data.data.length === 0) { // idk why it is result.data.data but otherwise it wont work
        return []
      }

      const rideGetDtos: RideGetDto[] = result.data.data.map((ride: RideGet) => ({
        id: ride.id,
        type: "other",
        departure_date: ride.departure_date,
        departure_time: ride.departure_time,
        arrival_time: ride.arrival_time,
        start_location: ride.start_location,
        end_location: ride.end_location,
        route_geometry: ride.route_geometry,
        n_available_seats: ride.max_n_codrives - ride.n_codrives,
        state: "default",
        image: `https://randomuser.me/api/portraits/women/${Math.floor(Math.random() * 99) + 1}.jpg`,
      } as RideGetDto));
      return rideGetDtos;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Abrufen der Fahrten.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  return {
    getEmptyRideCreate,
    postRide,
    getRidesForUser,
    getAllRides
  }
}
