import { defineStore } from "pinia";
import { ref, computed } from 'vue';
import { sortLocationItemPropsByTimeAsc, sortCodriveCardPropsByTimeAsc } from "@/services/utils";

import type { RideGetDto } from "@/types/Ride";
import type { RequestedCodriveGetDto, RouteUpdateDto, CodriverArrivalTimeGet, RequestedCodriveDto, CodriveGetDto } from "@/types/Codrive";
import type { LocationItemProps, CodriveCardProps } from "@/types/Props";

export const useMyRideStore = defineStore("myRide", () => {
  const ride = ref<RideGetDto | null>();

  // for displaying ride locations in "Meine Fahrt" screen
  const rideLocationItems = computed<LocationItemProps[]>(() => {
    if (!ride.value) {return [];} 

    let items: LocationItemProps[] = [
      {
        'location': ride.value.start_location, 
        'arrival_time': ride.value.departure_time,
        'arrival_date': ride.value.departure_date
      },
      ...ride.value.codrives.map(codrive => ({ 
        'location': codrive.location, 
        'arrival_time': codrive.arrival_time,
        'user': codrive.user,
      })),
      {
        'location': ride.value.end_location, 
        'arrival_time': ride.value.arrival_time,
        'arrival_date': ride.value.arrival_date
      }
    ];
    return sortLocationItemPropsByTimeAsc(items);
  }); 

  const requestedCodrive = ref<RequestedCodriveDto | null>();

  // for displaying codrives in "Meine Fahrt" screen
  const requestedCodriveCardItems = computed<CodriveCardProps[]>(() => {
    if (!ride.value) { return []; }
  
    // accepted codrives
    let accepted: CodriveCardProps[] = ride.value.codrives.map((codrive: CodriveGetDto) => ({
      codrive: codrive,
    } as CodriveCardProps));
    accepted = sortCodriveCardPropsByTimeAsc(accepted); 

    // not yet accepted codrives
    let requested: CodriveCardProps[] = ride.value.requested_codrives.map((codrive: RequestedCodriveGetDto) => ({
      requested_codrive: codrive,
    } as CodriveCardProps));
    requested = sortCodriveCardPropsByTimeAsc(requested);
    
    // fill the rest with empty codrives
    const empty = Array.from( {length: ride.value.n_available_seats}, () => ({} as CodriveCardProps)) // empty 
    
    return [...accepted, ...requested, ...empty];
  });

  const requestedCodriveLocationItems = computed<LocationItemProps[]>(() => {
    if (!ride.value || !requestedCodrive.value) {return [];} 

    let items: LocationItemProps[] = [
      {
        'location': ride.value.start_location, 
        'arrival_time': ride.value.departure_time,
        'updated_arrival_time': requestedCodrive.value.new_departure_time, 
        'arrival_date': requestedCodrive.value.new_departure_date,
      },
      ...requestedCodrive.value.route_update.map((routeUpdate: RouteUpdateDto)  => ({ 
        'location': routeUpdate.location, 
        'arrival_time': routeUpdate.arrival_time,
        'user': {
          first_name: routeUpdate.passenger_first_name,
          last_name: routeUpdate.passenger_last_name
        },
      } as LocationItemProps)),
      {
        'location': ride.value.end_location, 
        'arrival_time': ride.value.arrival_time,
        'arrival_date': ride.value.arrival_date
      }
    ];
    return sortLocationItemPropsByTimeAsc(items);
  }); 

  function setRide(newRide: RideGetDto) {
    ride.value = newRide;
  }

  function removeRide() {
    ride.value = null;
  }
  
  function setRequestedCodrive(codrive: RequestedCodriveGetDto) {
    requestedCodrive.value = {
      id: codrive.id,
      first_name: codrive.user.first_name,
      last_name: codrive.user.last_name,
      route_update: codrive.route_update.codriver_arrival_times.map((arrival: CodriverArrivalTimeGet) => ({
        location: arrival.location,
        passenger_first_name: arrival.user.first_name,
        passenger_last_name: arrival.user.last_name,
        arrival_date: arrival.arrival_date,
        arrival_time: arrival.arrival_time,
      } as RouteUpdateDto)),
      new_departure_date: codrive.route_update.updated_ride_departure_date,
      new_departure_time: codrive.route_update.updated_ride_departure_time,
      point_contribution: codrive.point_contribution,
      n_passengers: codrive.n_passengers,
      message: codrive.message
    } as RequestedCodriveDto
  }

  function removeRequestedCodrive() {
    requestedCodrive.value = null;
  }

   
  // BOOKED RIDES

  const bookedRide = ref<RideGetDto | null>();

  // for displaying ride locations in "Meine Mitfahrt" screen
  const bookedRideLocationItems = computed<LocationItemProps[]>(() => {
    if (!bookedRide.value) {return [];} 

    let items: LocationItemProps[] = [
      {
        'location': bookedRide.value.start_location, 
        'arrival_time': bookedRide.value.departure_time,
        'arrival_date': bookedRide.value.departure_date
      },
      ...bookedRide.value.codrives.map(codrive => ({ 
        'location': codrive.location, 
        'arrival_time': codrive.arrival_time,
        'user': codrive.user,
      })),
      {
        'location': bookedRide.value.end_location, 
        'arrival_time': bookedRide.value.arrival_time,
        'arrival_date': bookedRide.value.arrival_date
      }
    ];
    return sortLocationItemPropsByTimeAsc(items);
  }); 

  function setBookedRide(newRide: RideGetDto) {
    bookedRide.value = newRide;
  }
  
  function removeBookedRide() {
    bookedRide.value = null;
  }

  return {
    ride,
    rideLocationItems,
    requestedCodrive,
    requestedCodriveCardItems,
    requestedCodriveLocationItems,
    setRide,
    removeRide,
    setRequestedCodrive,
    removeRequestedCodrive,

    bookedRide,
    bookedRideLocationItems,
    setBookedRide,
    removeBookedRide,
  };
});
