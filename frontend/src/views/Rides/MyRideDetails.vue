<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import { ref } from 'vue';
import { useMyRideStore } from '@/stores/MyRideStore';
import { useRouter } from 'vue-router';
import LocationItem from '@/components/LocationItem.vue';
import CodriveCard from '@/components/CodriveCard.vue';
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal.vue';
import { useToaster } from '@/composables/useToaster';
import { useRide } from '@/composables/useRide';
import InformationItem from '@/components/InformationItem.vue';

// Variables 
const router = useRouter();
const myRideStore = useMyRideStore();

const { showToast } = useToaster();
const { deleteRide, markRideAsCompleted } = useRide();

const showDeleteModal = ref<boolean>(false);
const loading = ref<boolean>(false);

if (!myRideStore.ride) {
  router.push({ name: 'myRides' }) // in case there is no ride saved in the store
}

// Delete
const onRequestDelete = () => {
  showDeleteModal.value = true
}

const onConfirmDelete = async () => {
  showDeleteModal.value = false
  loading.value = true;
  try {
    if (myRideStore.ride?.id) {
      await deleteRide(myRideStore.ride?.id);
      myRideStore.removeRide();

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

// request payment
const onRequestPayment = async () => {
  try {

    if (!myRideStore.ride) throw Error("Ride is not available in pinia");

    loading.value = true;
    await markRideAsCompleted(myRideStore.ride?.id);

    showToast('success', 'Zahlung angefordert')
  } catch (error: unknown) {
    console.log(error);
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="view-container " :class="{'padding-bottom-hb-1': myRideStore.ride?.state !== 'payment requested (driver)'}">
    <PageTitle :goBack="true">Meine Fahrt</PageTitle>
    
    <h2>Fahrtverlauf</h2>
    <div class="component-list">
      <LocationItem
        v-for="item in myRideStore.rideLocationItems"
        :location="item.location"
        :arrival_time="item.arrival_time"
        :arrival_date="item.arrival_date"
        :user="item.user"
      />
    </div>
    
    <h2>Mitfahrer</h2>
    <div class="component-list">
      <CodriveCard
      v-for="(item, idx) in myRideStore.requestedCodriveCardItems"
      :codrive="item.codrive"
      :requested_codrive="item.requested_codrive"
      :seat_no="idx+1"
      />
    </div>
    
    <h2>Informationen</h2>
    <div class="component-list">
      <InformationItem v-if="myRideStore.ride && !(['request payment (driver)', 'payment requested (driver)'].includes(myRideStore.ride.state))"
        type=availableSeats
        :value=myRideStore.ride?.n_available_seats
      />
      <InformationItem
        type=pointReward
        :value=myRideStore.ride?.point_reward
      />
    </div>

    <HoverButton v-if="myRideStore.ride?.state !== 'payment requested (driver)'" :buttons='[
      myRideStore.ride?.state === "request payment (driver)"
        ? {variant: "primary", text: "Zahlung anfordern", onClick: onRequestPayment, loading: loading} 
        : {variant: "primary", color: "danger", text: "Löschen", onClick: onRequestDelete, loading: loading}]'
    />
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
</style>