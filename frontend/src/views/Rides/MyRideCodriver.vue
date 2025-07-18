<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import { ref } from 'vue';
import { useMyRideStore } from '@/stores/MyRideStore';
import { useRouter } from 'vue-router';
import LocationItem from '@/components/LocationItem.vue';
import HoverButton from '@/components/HoverButton.vue';

// Variables 
const router = useRouter();
const myRideStore = useMyRideStore();

const loading = ref<boolean>(false);

if (!myRideStore.ride && !myRideStore.requestedCodrive) {
  router.push({ name: 'myRides' }) // in case there is no ride or reqeusted codrive saved in the store
}

const onAcceptCodrive = () => {
  loading.value = true;
  console.log("Codrive akzeptiert")
  loading.value = false;
  router.go(-1);
}

const onRejectCodrive = () => {
  loading.value = true;
  console.log("Codrive abgelehnt")
  loading.value = false;
  router.go(-1);
}
</script>

<template>
  <div class="view-container padding-bottom-hb-2">
    <PageTitle :goBack="true">Meine Fahrt</PageTitle>
    
    <h2>Neuer Fahrtverlauf</h2>
    <div class="component-list">
      <LocationItem
        v-for="item in myRideStore.requestedCodriveLocationItems"
        :location="item.location"
        :arrival_time="item.arrival_time"
        :arrival_date="item.arrival_date"
        :updated_arrival_time="item.updated_arrival_time"
        :user="item.user"
      />
    </div>

    <h2>Informationen</h2>

    <HoverButton :buttons='[
      {variant: "primary", onClick: onAcceptCodrive, text: "Akzeptieren", loading: loading},
      {variant: "primary", color: "danger", onClick: onRejectCodrive, text: "Ablehnen", loading: loading}]'
    />
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