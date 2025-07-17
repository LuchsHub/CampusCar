<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import TabSwitcher from '@/components/TabSwitcher.vue';
import { ref, onMounted, computed, type ComputedRef } from 'vue';
import type { RideGetDto } from '@/types/Ride';
import { useRide } from '@/composables/useRide';
import { useAuthStore } from '@/stores/AuthStore';
import RideCard from '@/components/RideCard.vue';
import { sortRidesByDateAsc } from '@/services/utils';
import { useUser } from '@/composables/useUser';
import { useToaster } from '@/composables/useToaster';
import router from '@/router';

const { getRidesForUser } = useRide()
const { checkUserHasLicense } = useUser();
const { showToast } = useToaster();
const authStore = useAuthStore();

const activeTab = ref('Bevorstehend')
const tabs = ['Bevorstehend', 'Vergangen']

// Variables 
const userOwnRides = ref<RideGetDto[]>([]);
const hasLicense = ref<boolean>(true);

// fetch data async from backend when component gets loaded
onMounted(async () => {
  userOwnRides.value = await getRidesForUser(authStore.userId);
  hasLicense.value = await checkUserHasLicense();
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

const navigateToNextPage = () => {
  if (!hasLicense.value) {
    showToast('info', 'Lade zuerst deinen Führerschein hoch.');
    return
  }
  router.push('/create_ride');
}
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
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
    <HoverButton :buttons='[{variant: "primary", text: "Fahrt anbieten", onClick: navigateToNextPage, disabled: !hasLicense}]'/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>