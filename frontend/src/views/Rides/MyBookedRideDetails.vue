<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import { onMounted, ref } from 'vue';
import { useMyRideStore } from '@/stores/MyRideStore';
import { useRouter } from 'vue-router';
import LocationItem from '@/components/LocationItem.vue';
import { useToaster } from '@/composables/useToaster';
import InformationItem from '@/components/InformationItem.vue';
import { useCodrive } from '@/composables/useCodrive';
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal.vue';
import ProfileCard from '@/components/ProfileCard.vue';
import RatingModal from '@/components/RatingModal.vue';
import { useUser } from '@/composables/useUser';

// Variables 
const router = useRouter();
const myRideStore = useMyRideStore();

const { showToast } = useToaster();
const { deleteBookedCodrive, payForCodrive } = useCodrive();
const { getUserBalance } = useUser();

const loading = ref<boolean>(false);
const showDeleteModal = ref<boolean>(false);
const showRatingModal = ref<boolean>(false);
const currentBalance = ref<number>(Infinity)

if (!myRideStore.bookedRide) {
  router.push({ name: 'myRides' }) // in case there is no ride saved in the store
}

onMounted(async () => {
  currentBalance.value = await getUserBalance();
})

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

// Payment
const onRequestPayment = () => {
  showRatingModal.value = true
}

const onConfirmRating = async (rating: number) => {
  try {
    if (!myRideStore.bookedRide?.codrive_id) throw Error('No booked ride saved in pinia.');
    loading.value = true;
    await payForCodrive(myRideStore.bookedRide.codrive_id, rating);
    showToast('success', 'Bezahlung erfolgreich.');
    router.go(-1);
  } catch (error: unknown) {
    showToast("error", "Zu wenig Guthaben");
    console.log(error);
  } finally {
    loading.value = false;
  }
}

const onCancelRating = () => {
  showRatingModal.value = false
}
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
    <PageTitle :goBack="true">Meine Mitfahrt</PageTitle>
    
    <h2>Fahrer</h2>
    <ProfileCard v-if="myRideStore.bookedRide"
      :first_name="myRideStore.bookedRide.driver.first_name"
      :last_name="myRideStore.bookedRide.driver.last_name"
      :avg_rating="myRideStore.bookedRide.driver.avg_rating"
      :profile_picture="myRideStore.bookedRide.image"
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
        :value=(Number(myRideStore.bookedRide?.point_cost)/100).toFixed(2)
      />

      <!-- ERRORS -->
      <div v-if="myRideStore.bookedRide?.state === 'payment not requested yet (codriver)'" class="margin-botton-l error-message-container">
        <p class="text-danger">Du kannst die Fahrt noch nicht bezahlen, da der Fahrer die Zahlung noch nicht angefordert hat.</p>
      </div>
      <div v-if="myRideStore.bookedRide && currentBalance < Number(myRideStore.bookedRide.point_cost)/100" class="margin-botton-l error-message-container">
        <p class="text-danger">Du hast nicht genügend Guthaben, um die Fahrt zu bezahlen. Lade zuerst Guthaben in deinem Profil auf.</p>
      </div>
    </div>

    <HoverButton v-if="myRideStore.bookedRide && myRideStore.bookedRide.state !== 'finished'" :buttons='[
      ["payment outstanding (codriver)", "payment not requested yet (codriver)"].includes(myRideStore.bookedRide.state)
      ? {variant: "primary", onClick: onRequestPayment, text: "Mitfahrt bezahlen", disabled: (myRideStore.bookedRide?.state === "payment not requested yet (codriver)" || currentBalance < Number(myRideStore.bookedRide.point_cost)/100), loading: loading}
      : {variant: "primary", color: "danger", onClick: onRequestDelete, text: "Mitfahrt absagen", loading: loading}]'
    />
  </div>
  <ConfirmDeleteModal
    :open="showDeleteModal"
    subject="Mitfahrt"
    :requiresTextConfirmation="false"
    @confirm="onConfirmCodriveDelete"
    @cancel="onCancelDelete"
  />
  <RatingModal v-if="myRideStore.bookedRide"
    :open="showRatingModal"
    :driver_first_name="myRideStore.bookedRide.driver.first_name"
    :cost="Number(myRideStore.bookedRide.point_cost)"
    @confirm="onConfirmRating"
    @cancel="onCancelRating"
  />
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>