<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';
import { ref } from 'vue';
import type { RideGetDto } from '@/types/Ride';
import { useRideStore } from '@/stores/RideStore';
import { useRouter } from 'vue-router';

// Variables 
const router = useRouter();
const rideStore = useRideStore();
const ride = ref<RideGetDto | null>();

if (!rideStore.ride) {
  router.push({ name: 'myRides' }) // in case there is no ride saved in the store
} else {
  ride.value = rideStore.ride;
}

const hoverButtons: ButtonProps[] = [
    {variant: "secondary", text: "Bearbeiten"},
    {variant: "primary", color: "danger", text: "Löschen"},
]

console.log(ride.value?.arrival_time);
</script>

<template>
  <div class="view-container">
    <PageTitle :goBack="true">Meine Fahrt</PageTitle>
    <h2>Fahrtverlauf</h2>
    <p>{{ ride?.arrival_time }}</p>
    <HoverButton :buttons="hoverButtons"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>