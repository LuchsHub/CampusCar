<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';
import TabSwitcher from '@/components/TabSwitcher.vue';
import { ref, onMounted, computed, type ComputedRef } from 'vue';
import type { RideGetDto } from '@/types/Ride';
import { useRide } from '@/composables/useRide';
import { useAuthStore } from '@/stores/AuthStore';
import RideCard from '@/components/RideCard.vue';
import { sortRidesByDateAsc } from '@/services/utils';

const { getRidesForUser } = useRide()
const authStore = useAuthStore();

const activeTab = ref('Bevorstehend')
const tabs = ['Bevorstehend', 'Vergangen']

const hoverButtons: ButtonProps[] = [
    {variant: "primary", text: "Fahrt anbieten", to: "/create_ride"},
]

// Variables 
const userOwnRides = ref<RideGetDto[]>([]);

// fetch data async from backend when component gets loaded
onMounted(async () => {
  userOwnRides.value = await getRidesForUser(authStore.userId);
})

const sortedRides: ComputedRef<RideGetDto[]> = computed(() => {
  return sortRidesByDateAsc(userOwnRides.value);
});

const now = () => new Date();

const upcomingRides = computed<RideGetDto[]>(() =>
  sortedRides.value.filter(ride => {
    const rideDate = new Date(`${ride.departure_date}T${ride.departure_time}`);
    return rideDate >= now();
  })
);

const pastRides = computed<RideGetDto[]>(() =>
  sortedRides.value.filter(ride => {
    const rideDate = new Date(`${ride.departure_date}T${ride.departure_time}`);
    return rideDate < now();
  })
);
</script>

<template>
  <div class="view-container" :class="`padding-bottom-hb-${hoverButtons.length}`">
    <PageTitle>Meine Fahrten</PageTitle>

    <TabSwitcher v-model="activeTab" :tabs="tabs" />
      
    <div v-if="activeTab === 'Bevorstehend'" class="width-100">
        <template v-for="(ride, index) in upcomingRides" :key="ride.id">
          <RideCard :ride="ride"/>
          <hr v-if="index < upcomingRides.length - 1" />
        </template>
      </div>
    
      <div v-else class="width-100">
        <template v-for="(ride, index) in pastRides" :key="ride.id">
          <RideCard
            :ride="ride"
            type="own"
            state="accepted"
          />
          <hr v-if="index < pastRides.length - 1" />
        </template>
      </div>
    <HoverButton :buttons="hoverButtons"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>