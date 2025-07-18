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

// Variables 
const router = useRouter();
const myRideStore = useMyRideStore();

const { showToast } = useToaster();
const { deleteRide } = useRide();

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
</script>

<template>
  <div class="view-container padding-bottom-hb-2">
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
      :state="item.state"
      :codrive="item.codrive"
      :seat_no="idx+1"
      />
    </div>
    
    <h2>Informationen</h2>

    <HoverButton :buttons='[
      {variant: "secondary", text: "Bearbeiten"},
      {variant: "primary", color: "danger", onClick: onRequestDelete, text: "Löschen"}]'
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

.component-list {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: 100%;
  gap: var(--horizontal-gap)
}
</style>