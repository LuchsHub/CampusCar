<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';
import TabSwitcher from '@/components/TabSwitcher.vue';
import { ref, onMounted } from 'vue';
import type { RideGet } from '@/types/Ride';
import { useRide } from '@/types/useRide';
import { useAuthStore } from '@/stores/AuthStore';
import RideCard from '@/components/RideCard.vue';

const { getRidesForUser } = useRide()
const authStore = useAuthStore();

const activeTab = ref('Bevorstehend')
const tabs = ['Bevorstehend', 'Vergangen']

const hoverButtons: ButtonProps[] = [
    {variant: "primary", text: "Fahrt anbieten", to: "/create_ride"},
]

// Variables 
const userRides = ref<RideGet[]>([]);

// fetch data async from backend when component gets loaded
onMounted(async () => {
  userRides.value = await getRidesForUser(authStore.userId);
  console.log(userRides.value);
})
</script>

<template>
  <div class="view-container">
    <PageTitle>Meine Fahrten</PageTitle>

    <TabSwitcher v-model="activeTab" :tabs="tabs" />
      
    <div v-if="activeTab === 'Bevorstehend'" class="width-100">
        <template v-for="(ride, index) in userRides" :key="ride.id">
          <RideCard
            :ride="ride"
            type="own"
            state="accepted"
          />
          <hr v-if="index < userRides.length - 1" />
        </template>
      </div>
    
      <div v-else>
        <h2>Vergangen</h2>
      </div>
    <HoverButton :buttons="hoverButtons"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>