<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import { ref } from 'vue';
import { useMyRideStore } from '@/stores/MyRideStore';
import { useRouter } from 'vue-router';
import LocationItem from '@/components/LocationItem.vue';
import HoverButton from '@/components/HoverButton.vue';
import InformationItem from '@/components/InformationItem.vue';
import { useCodrive } from '@/composables/useCodrive';
import { useToaster } from '@/composables/useToaster';
import ProfileCard from '@/components/ProfileCard.vue';
import { useRide } from '@/composables/useRide';

// Variables 
const router = useRouter();
const myRideStore = useMyRideStore();
const { acceptCodrive, rejectCodrive } = useCodrive();
const { showToast } = useToaster();
const { getRideById } = useRide();

const loadingAccept = ref<boolean>(false);
const loadingReject = ref<boolean>(false);

if (!myRideStore.ride && !myRideStore.requestedCodrive) {
  router.push({ name: 'myRides' }) // in case there is no ride or reqeusted codrive saved in the store
}

const onAcceptCodrive = async () => {
  loadingAccept.value = true;
  try {

    // check if ride or codrive exist in store
    if (!myRideStore.requestedCodrive || !myRideStore.ride) {
      throw Error('No Codrive or Ride is saved in pinia.');
    }

    await acceptCodrive(myRideStore.requestedCodrive.id);

    // update ride in store
    const updatedRide = await getRideById(myRideStore.ride.id);
    myRideStore.setRide(updatedRide);

    // success
    showToast('success', 'Mitfahrt akzeptiert.');
    router.go(-1);
  } catch (error: unknown) {
    console.log(error);     
  }
  finally {
    loadingAccept.value = false;
  }
}

const onRejectCodrive = async () => {
  loadingReject.value = true;
  try {
    
    // check 
    if (!myRideStore.requestedCodrive || !myRideStore.ride) {
      throw Error('No Codrive or Ride is saved in pinia.');
    }

    await rejectCodrive(myRideStore.requestedCodrive.id);

    // fetch new ride and put in store 
    const updatedRide = await getRideById(myRideStore.ride.id);
    myRideStore.setRide(updatedRide);

    showToast('success', 'Mitfahrt abgelehnt.');
    router.go(-1);
  } catch (error: unknown) {
    console.log(error);     
  }
  finally {
    loadingReject.value = false;
  }
}
</script>

<template>
  <div class="view-container padding-bottom-hb-2">
    <PageTitle :goBack="true">Angefragte Mitfahrt</PageTitle>

    <h2>Mitfahrer</h2>
    <ProfileCard v-if="myRideStore.requestedCodrive"
      :first_name="myRideStore.requestedCodrive.first_name"
      :last_name="myRideStore.requestedCodrive.last_name"
      :avg_rating="myRideStore.requestedCodrive.avg_rating"
      :profile_picture="myRideStore.requestedCodrive.image"
    />
    
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
    <div class="component-list">
      <InformationItem
        type=bookedSeats
        :value=myRideStore.requestedCodrive?.n_passengers
      />
      <InformationItem
        type=pointReward
        :value=myRideStore.requestedCodrive?.point_contribution
      />
      <InformationItem v-if="myRideStore.requestedCodrive?.message"
        type=message
        :value=myRideStore.requestedCodrive?.message
      />
    </div>

    <HoverButton :buttons='[
      {variant: "primary", onClick: onAcceptCodrive, text: "Akzeptieren", loading: loadingAccept},
      {variant: "primary", color: "danger", onClick: onRejectCodrive, text: "Ablehnen", loading: loadingReject}]'
    />
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>