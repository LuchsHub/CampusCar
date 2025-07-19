import { reactive } from 'vue';
import type { RideCreateBase, RideGet, RideGetDto } from '../types/Ride';
import type { RideCreateComplete } from '../types/Ride';
import api from '@/services/api';
import axios from 'axios';
import { useToaster } from '@/composables/useToaster';
import type { LocationCreateDto } from '../types/Location';
import type { CodriveGetDto, MyCodriveGet } from '@/types/Codrive';
import { useUser } from './useUser';


export function useRide() {
  
  const { showDefaultError, showToast } = useToaster()
  const { getProfileImageUrl } = useUser();

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
    ride.max_request_distance = (Number(ride.max_request_distance) * 1000).toString() // convert to meters
    try {
      await api.post(
        '/rides',
        ride
      );
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Erstellen der Fahrt.');
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

      const rideGetDtos: RideGetDto[] = await Promise.all(
        result.data.data.map(async (ride: RideGet) => ({
          id: ride.id,
          driver: ride.driver,
          type: "other",
          departure_time: ride.departure_time,
          departure_date: ride.departure_date,
          arrival_time: ride.arrival_time,
          arrival_date: ride.arrival_date,
          start_location: ride.start_location,
          end_location: ride.end_location,
          route_geometry: ride.route_geometry,
          n_available_seats: ride.max_n_codrives - ride.n_codrives,
          codrives: ride.codrives,
          requested_codrives: ride.requested_codrives,
          max_request_distance: ride.max_request_distance,
          state: "default",
          image: await getProfileImageUrl(ride.driver.id),
      } as RideGetDto)))
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

  const getRidesForUser = async (): Promise<RideGetDto[]> => {
    try {
      const result = await api.get(`/rides/me`);

      if (result.data.data.length === 0) { // idk why it is result.data.data but otherwise it wont work
        return []
      }

      const rideGetDtos: RideGetDto[] = result.data.data.map((ride: RideGet) => ({
        id: ride.id,
        driver: ride.driver,
        type: "own",
        departure_time: ride.departure_time,
        departure_date: ride.departure_date,
        arrival_time: ride.arrival_time,
        arrival_date: ride.arrival_date,
        start_location: ride.start_location,
        end_location: ride.end_location,
        route_geometry: ride.route_geometry,
        n_available_seats: ride.max_n_codrives - ride.n_codrives,
        codrives: ride.codrives,
        requested_codrives: ride.requested_codrives,
        state: ride.requested_codrives.length === 0 ? "default" : "new request",
        point_reward: ride.codrives
          .reduce((sum: number, codrive: CodriveGetDto) => sum + codrive.point_contribution, 0)
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

  const getBookedRidesForUser = async (): Promise<RideGetDto[]> => {
    try {
      const result = await api.get(`/codrives/me`);

      if (result.data.data.length === 0) { // idk why it is result.data.data but otherwise it wont work
        return []
      }

      const codrive = result.data.data;
      const rideGetDtos: RideGetDto[] = codrive.map((codrive: MyCodriveGet) => ({
        id: codrive.ride.id,
        type: "booked",
        codrive_id: codrive.id,
        departure_time: codrive.ride.departure_time,
        departure_date: codrive.ride.departure_date,
        arrival_time: codrive.ride.arrival_time,
        arrival_date: codrive.ride.arrival_date,
        start_location: codrive.ride.start_location,
        end_location: codrive.ride.end_location,
        codrives: codrive.ride.codrives,
        state: codrive.accepted ? 'accepted' : 'not accepted yet',
        point_cost: codrive.point_contribution
      } as RideGetDto));
      return rideGetDtos;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Abrufen deiner gebuchten Fahrten.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  const getRideById = async (rideId: string): Promise<RideGetDto> => {
    try {
      const result = await api.get(`/rides/${rideId}`);
      const ride = result.data;
      const rideDto: RideGetDto = {
        id: ride.id,
        driver: ride.driver,
        type: "own",
        departure_time: ride.departure_time,
        departure_date: ride.departure_date,
        arrival_time: ride.arrival_time,
        arrival_date: ride.arrival_date,
        start_location: ride.start_location,
        end_location: ride.end_location,
        route_geometry: ride.route_geometry,
        n_available_seats: ride.max_n_codrives - ride.n_codrives,
        codrives: ride.codrives,
        requested_codrives: ride.requested_codrives,
        state: ride.requested_codrives.length === 0 ? "default" : "new request",
        point_reward: ride.codrives
          .reduce((sum: number, codrive: CodriveGetDto) => sum + codrive.point_contribution, 0)
      } as RideGetDto
      return rideDto;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Abrufen der Fahrt.');
      } else {
        showDefaultError();
      }
      throw error
    }
  }

  const deleteRide = async (rideId: string): Promise<void> => {
    try {
      await api.delete(`/rides/${rideId}`);
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Löschen der Fahrt.');
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
    getAllRides,
    getRideById,
    deleteRide,
    getBookedRidesForUser
  }
}
