<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import TabSwitcher from '@/components/TabSwitcher.vue';
import { ref, onMounted, computed, type ComputedRef } from 'vue';
import type { RideGetDto } from '@/types/Ride';
import { useRide } from '@/composables/useRide';
import RideCard from '@/components/RideCard.vue';
import { sortRidesByDateAsc } from '@/services/utils';

const { getRidesForUser, getBookedRidesForUser } = useRide()

const activeTab = ref('Bevorstehend')
const tabs = ['Bevorstehend', 'Vergangen']

// Variables 
const userOwnRides = ref<RideGetDto[]>([]);
const userBookedRides = ref<RideGetDto[]>([]);

// fetch data async from backend when component gets loaded
onMounted(async () => {
  userOwnRides.value = await getRidesForUser();
  userBookedRides.value = await getBookedRidesForUser();
})

const sortedRides: ComputedRef<RideGetDto[]> = computed(() => {
  return sortRidesByDateAsc([...userOwnRides.value, ...userBookedRides.value]);
});

const upcomingRides = computed<RideGetDto[]>(() =>
  sortedRides.value.filter(ride => {
    const rideDate = new Date(`${ride.arrival_date}T${ride.arrival_time}`);
    return rideDate >= new Date();
  })
);

const pastRides = computed<RideGetDto[]>(() =>
  sortedRides.value.filter(ride => {
    const rideDate = new Date(`${ride.arrival_date}T${ride.arrival_time}`);
    return rideDate < new Date();
  })
);
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
    <PageTitle>Meine Fahrten</PageTitle>

    <TabSwitcher v-model="activeTab" :tabs="tabs" />
      
    <div v-if="activeTab === 'Bevorstehend'" class="width-100">
        <template v-for="(ride, index) in upcomingRides" :key="ride.id">
          <RideCard 
            :ride="ride"
          />
          <hr v-if="index < upcomingRides.length - 1" />
        </template>
      </div>
    
      <div v-else class="width-100">
        <template v-for="(ride, index) in pastRides" :key="ride.id">
          <RideCard
            :ride="ride"
          />
          <hr v-if="index < pastRides.length - 1" />
        </template>
      </div>
    <HoverButton :buttons='[{variant: "primary", text: "Fahrt anbieten", to: "create_ride"}]'/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>