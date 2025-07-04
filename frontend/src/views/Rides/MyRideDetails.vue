<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps, CodriveCardProps } from '@/types/Props';
import { ref, computed } from 'vue';
import type { RideGetDto } from '@/types/Ride';
import { useRideStore } from '@/stores/RideStore';
import { useRouter } from 'vue-router';
import type { LocationItemProps } from '@/types/Props';
import LocationItem from '@/components/LocationItem.vue';
import { sortLocationItemPropsByTimeAsc, sortCodriveCardPropsByTimeAsc } from '@/services/utils';
import CodriveCard from '@/components/CodriveCard.vue';
import type { CodriveGetDto } from '@/types/Codrive';

// Variables 
const router = useRouter();
const rideStore = useRideStore();
const ride = ref<RideGetDto | null>();
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

const codriveCardItems = computed<CodriveCardProps[]>(() => {
  if (!ride.value) { return []; }
  let accepted: CodriveCardProps[] = ride.value.codrives.map((codrive: CodriveGetDto) => ({
    codrive: codrive,
    codrive_accepted: true
  } as CodriveCardProps));
  accepted = sortCodriveCardPropsByTimeAsc(accepted); 
  const notAccepted: CodriveCardProps[] = ride.value.requested_codrives.map((codrive: CodriveGetDto) => ({
    codrive: codrive,
    codrive_accepted: false
  } as CodriveCardProps));
  return [...accepted, ...notAccepted];
});

if (!rideStore.ride) {
  router.push({ name: 'myRides' }) // in case there is no ride saved in the store
} else {
  ride.value = rideStore.ride;
}

const hoverButtons: ButtonProps[] = [
    {variant: "secondary", text: "Bearbeiten"},
    {variant: "primary", color: "danger", text: "Löschen"},
]
</script>

<template>
  <div class="view-container">
    <PageTitle :goBack="true">Meine Fahrt</PageTitle>
    
    <h2>Fahrtverlauf</h2>
    <div class="component-list">
      <LocationItem
        v-for="item in rideLocationItems"
        :location="item.location"
        :arrival_time="item.arrival_time"
        :arrival_date="item.arrival_date"
        :user="item.user"
      />
    </div>
    
    <h2>Mitfahrer</h2>
    <HoverButton :buttons="hoverButtons"/>
    <div class="component-list">
      <CodriveCard
        v-for="(item, idx) in codriveCardItems"
        :codrive_accepted="item.codrive_accepted"
        :codrive="item.codrive"
        :seat_no="idx+1"
      />
    </div>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}

.component-list {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: 100%;
  gap: var(--horizontal-gap)
}
</style>