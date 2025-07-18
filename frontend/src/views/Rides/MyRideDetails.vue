<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { CodriveCardProps } from '@/types/Props';
import { ref, computed } from 'vue';
import type { RideGetDto } from '@/types/Ride';
import { useRideStore } from '@/stores/RideStore';
import { useRouter } from 'vue-router';
import type { LocationItemProps } from '@/types/Props';
import LocationItem from '@/components/LocationItem.vue';
import { sortLocationItemPropsByTimeAsc, sortCodriveCardPropsByTimeAsc } from '@/services/utils';
import CodriveCard from '@/components/CodriveCard.vue';
import type { CodriveGetDto } from '@/types/Codrive';
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal.vue';
import { useToaster } from '@/composables/useToaster';
import { useRide } from '@/composables/useRide';

// Variables 
const router = useRouter();
const rideStore = useRideStore();
const ride = ref<RideGetDto | null>();

const { showToast } = useToaster();
const { deleteRide } = useRide();

const showDeleteModal = ref<boolean>(false);
const loading = ref<boolean>(false);

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

  // accepted codrives
  let accepted: CodriveCardProps[] = ride.value.codrives.map((codrive: CodriveGetDto) => ({
    state: "accepted",
    codrive: codrive,
  } as CodriveCardProps));
  accepted = sortCodriveCardPropsByTimeAsc(accepted); 

  // not yet accepted codrives
  let notAccepted: CodriveCardProps[] = ride.value.requested_codrives.map((codrive: CodriveGetDto) => ({
    state: "notAccepted",
    codrive: codrive,
  } as CodriveCardProps));
  notAccepted = sortCodriveCardPropsByTimeAsc(notAccepted);

  // fill the rest with empty codrives
  const no_empty_seats = ride.value.n_available_seats - (accepted.length + notAccepted.length);
  const empty = Array.from( {length: no_empty_seats}, () => ({
    state: "empty"
  } as CodriveCardProps))

  return [...accepted, ...notAccepted, ...empty];
});

if (!rideStore.ride) {
  router.push({ name: 'myRides' }) // in case there is no ride saved in the store
} else {
  ride.value = rideStore.ride;
}

// Delete
const onRequestDelete = () => {
  showDeleteModal.value = true
}

const onConfirmDelete = async () => {
  showDeleteModal.value = false
  loading.value = true;
  try {
    if (ride.value?.id) {
      await deleteRide(ride.value.id);
    } else {
      throw new Error('No ride ID found for deletion.');
    }
    showToast('success', 'Fahrt gelöscht.')
    router.push('/my_rides')
  }
  catch (error: unknown) {
    console.log(error);
  }
  finally {
    loading.value = false;
  }
}

const onCancelDelete = () => {
  showDeleteModal.value = false
}
</script>

<template>
  <div class="view-container padding-bottom-hb-2">
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
    <HoverButton :buttons='[
      {variant: "secondary", text: "Bearbeiten"},
      {variant: "primary", color: "danger", onClick: onRequestDelete, text: "Löschen"}]'
    />
    <div class="component-list">
      <CodriveCard
      v-for="(item, idx) in codriveCardItems"
      :state="item.state"
      :codrive="item.codrive"
      :seat_no="idx+1"
      />
    </div>

    <h2>Informationen</h2>
  </div>
  <ConfirmDeleteModal
    :open="showDeleteModal"
    @confirm="onConfirmDelete"
    @cancel="onCancelDelete"
  />
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