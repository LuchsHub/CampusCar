import { reactive } from 'vue';
import type { RideCreateBase, RideGet, RideGetDto, RideCreateComplete, RideState } from '../types/Ride';
import api from '@/services/api';
import axios from 'axios';
import { useToaster } from '@/composables/useToaster';
import type { LocationCreateDto } from '../types/Location';
import type { CodriveGetDto, MyCodriveGet, RequestedCodriveGetDto } from '@/types/Codrive';
import { useUser } from './useUser';

export function useRide() {
  
  const { showDefaultError, showToast } = useToaster()
  const { getProfileImageUrl, getUserMe } = useUser();

  const getEmptyRideCreate = (): RideCreateBase => {
    return reactive<RideCreateBase>({
        car_id: "",
        max_n_codrives: 0,
        max_request_distance: 0,
        arrival_time: "",
        arrival_date: "",
    })
  }

  const checkIfRideIsOver = ( arrival_date: string, arrival_time: string) => {
    const dateTimeString = `${arrival_date}T${arrival_time}`;
    const rideEndDate = new Date(dateTimeString);
    return rideEndDate < new Date();
}

  const checkBookedRideState = (accepted: boolean, paid: boolean, completed: boolean, arrivalDate: string, arrivalTime: string): RideState => {
    if (!accepted) {
      return "not accepted yet";
    } else if (!checkIfRideIsOver(arrivalDate, arrivalTime)) {
      return "accepted";
    } else if (!paid && !completed) {
      return "payment not requested yet (codriver)";
    } else if (!paid && completed) {
      return "payment outstanding (codriver)";
    } else {
      return "finished";
    }
  }
  
  const checkOwnRideState = (requestedCodrives: RequestedCodriveGetDto[], completed: boolean, arrivalDate: string, arrivalTime: string): RideState => {
    if (requestedCodrives.length > 0) {
      return "new request";
    } else if (checkIfRideIsOver(arrivalDate, arrivalTime) && !completed) {
      return "request payment (driver)";
    } else if (checkIfRideIsOver(arrivalDate, arrivalTime) && completed) {
      return "payment requested (driver)";
    } else {
      return "default"
    }
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

  const getAllRidesWithMaxDistance = async (
  maxDistanceKm: number = 30
): Promise<RideGetDto[]> => {
  try {
    const result = await api.get('/rides', {
      params: {
        offset: 0,
        limit: 100,
        max_distance_km: maxDistanceKm,
      },
    })

    if (!result.data.data || result.data.data.length === 0) {
      return []
    }

    const currentUser = await getUserMe()
    const currentUserId = currentUser?.id

    const rideGetDtos: RideGetDto[] = await Promise.all(
      result.data.data.map(async (ride: RideGet) => {
        const isInCodrive = currentUserId
          ? isUserInCodrivesOrRequests(currentUserId, ride.codrives, ride.requested_codrives)
          : false

        const rideDto: RideGetDto = {
          id: ride.id,
          driver: ride.driver,
          type: 'other',
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
          max_request_distance: typeof ride.max_request_distance === 'number'
            ? ride.max_request_distance
            : Number(ride.max_request_distance),
          state: isInCodrive ? 'not visible' : 'default',
          completed: ride.completed,
          image: (await getProfileImageUrl(ride.driver.id)) ?? ''
        }

        return rideDto
      })
    )

    return rideGetDtos
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      showToast('error', 'Fehler beim Abrufen der Fahrten.')
    } else {
      showDefaultError()
    }
    throw error
  }
}

  const isUserInCodrivesOrRequests = (
    userId: string,
    codrives: CodriveGetDto[],
    requestedCodrives: RequestedCodriveGetDto[]
  ): boolean => {
    return (
      codrives.some((c) => typeof c.codriver === 'object' && c.codriver?.id === userId) ||
      requestedCodrives.some((r) => typeof r.codriver === 'object' && r.codriver?.id === userId)
    )
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
        state: checkOwnRideState(ride.requested_codrives, ride.completed, ride.arrival_date, ride.arrival_time),
        completed: ride.completed,
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
      
      const codrive: MyCodriveGet[] = result.data.data;

      const rideGetDtos: RideGetDto[] = await Promise.all(
        codrive.map(async (codrive: MyCodriveGet) => ({
          id: codrive.ride.id,
          driver: codrive.ride.driver,
          type: "booked",
          codrive_id: codrive.id,
          departure_time: codrive.ride.departure_time,
          departure_date: codrive.ride.departure_date,
          arrival_time: codrive.ride.arrival_time,
          arrival_date: codrive.ride.arrival_date,
          start_location: codrive.ride.start_location,
          end_location: codrive.ride.end_location,
          codrives: codrive.ride.codrives,
          state: checkBookedRideState(codrive.accepted, codrive.paid, codrive.ride.completed ,codrive.ride.arrival_date, codrive.ride.arrival_time),
          completed: codrive.ride.completed,
          point_cost: codrive.point_contribution,
          image: await getProfileImageUrl(codrive.ride.driver.id),
        } as RideGetDto)))
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
        completed: ride.completed,
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

  const markRideAsCompleted = async (rideId: string): Promise<void> => {
    try {
      await api.patch(`rides/${rideId}/complete`);
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        showToast('error', 'Fehler beim Abschließen der Fahrt.');
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
    getBookedRidesForUser,
    markRideAsCompleted,
    checkIfRideIsOver,
    getAllRidesWithMaxDistance 
  }
}
