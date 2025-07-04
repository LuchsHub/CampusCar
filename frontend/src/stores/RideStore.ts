import type { RideGetDto } from "@/types/Ride";
import { defineStore } from "pinia";
import { ref } from 'vue';

export const useRideStore = defineStore("ride", () => {
  const ride = ref<RideGetDto | null>();

  function setRide(newRide: RideGetDto) {
    ride.value = newRide;
  }

  function removeRide() {
    ride.value = null;
  }

  return {
    ride,
    setRide,
    removeRide,
  };
});
