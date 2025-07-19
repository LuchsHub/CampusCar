<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import { ref } from 'vue';
import { useMyRideStore } from '@/stores/MyRideStore';
import { useRouter } from 'vue-router';
import LocationItem from '@/components/LocationItem.vue';
import { useToaster } from '@/composables/useToaster';
import InformationItem from '@/components/InformationItem.vue';
import { useCodrive } from '@/composables/useCodrive';
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal.vue';
import ProfileCard from '@/components/ProfileCard.vue';

// Variables 
const router = useRouter();
const myRideStore = useMyRideStore();

const { showToast } = useToaster();
const { deleteBookedCodrive } = useCodrive();

const loading = ref<boolean>(false);
const showDeleteModal = ref<boolean>(false);

if (!myRideStore.bookedRide) {
  router.push({ name: 'myRides' }) // in case there is no ride saved in the store
}

// Delete
const onConfirmCodriveDelete = async () => {
  showDeleteModal.value = false
  loading.value = true;
  try {
    if (!myRideStore.bookedRide || !myRideStore.bookedRide.codrive_id) {
      throw Error('No booked ride saved in pinia.');
    }
    await deleteBookedCodrive(myRideStore.bookedRide.codrive_id);
    showToast('success', 'Mitfahrt abgesagt.');
    router.go(-1);
  } catch (error: unknown) {
    console.log(error);
  } finally {
    loading.value = false;
  }
}

const onRequestDelete = () => {
  showDeleteModal.value = true
}

const onCancelDelete = () => {
  showDeleteModal.value = false
}
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
    <PageTitle :goBack="true">Meine Mitfahrt</PageTitle>
    
    <h2>Fahrer</h2>
    <ProfileCard v-if="myRideStore.ride"
      :first_name="myRideStore.ride.driver.first_name"
      :last_name="myRideStore.ride.driver.last_name"
      :avg_rating="myRideStore.ride.driver.avg_rating"
      :profile_picture="myRideStore.ride.image"
    />
    
    <h2>Fahrtverlauf</h2>
    <div class="component-list">
      <LocationItem
        v-for="item in myRideStore.bookedRideLocationItems"
        :location="item.location"
        :arrival_time="item.arrival_time"
        :arrival_date="item.arrival_date"
        :user="item.user"
      />
    </div>
    
    <h2>Informationen</h2>
    <div class="component-list">
      <InformationItem
        type=pointCost
        :value=myRideStore.bookedRide?.point_cost
      />
    </div>

    <HoverButton :buttons='[
      {variant: "primary", color: "danger", onClick: onRequestDelete, text: "Mitfahrt absagen", loading: loading}]'
    />
  </div>
  <ConfirmDeleteModal
    :open="showDeleteModal"
    @confirm="onConfirmCodriveDelete"
    @cancel="onCancelDelete"
  />
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>