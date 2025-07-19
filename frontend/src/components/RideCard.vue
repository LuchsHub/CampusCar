<script setup lang="ts">
import type { RideCardProps } from '@/types/Props';
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { Users, Car } from 'lucide-vue-next';
import { useMyRideStore } from '@/stores/MyRideStore';
import { formatTime, formatDate } from '@/services/utils';

const props = defineProps<RideCardProps>();
const router = useRouter();
const myRideStore = useMyRideStore();

const stateInfo = computed(() => {
  switch (props.ride.state) {
    case 'new request':
      return { message: 'Neue Anfrage', infoTextClass: 'text-info', standardTextClass: 'text-neutral-900'}
    case 'not accepted yet':
      return { message: 'Noch nicht akzeptiert', infoTextClass: 'text-warning' , standardTextClass: 'text-neutral-400'}
    case 'accepted':
      return { message: 'Angenommen', infoTextClass: 'text-success', standardTextClass: 'text-neutral-900'}
    case 'rejected':
      return { message: 'Abgelehnt', infoTextClass: 'text-danger', standardTextClass: 'text-neutral-400 text-strikethrough'}
    case 'payment outstanding':
      return { message: 'Zahlung ausstehend', infoTextClass: 'text-danger', standardTextClass: 'text-neutral-400'}
    default:
      return { message: '', infoTextClass: ''}
  }
})

const goToRideDetailsScreen = () => {
  if (props.ride.type === 'own') {
    myRideStore.setRide(props.ride);
    router.push({ name: 'myRideDetails' });
  } else if (props.ride.type === 'booked' && ['accepted', 'payment outstanding'].includes(props.ride.state)) {
    myRideStore.setBookedRide(props.ride);
    router.push({ name: 'myBookedRideDetails' });
  }else if (props.ride.type === 'other'){
    myRideStore.setRide(props.ride);
    router.push({ name: 'RideRequest' });
  }
}
</script>

<template>
<div 
  class="ride-card-container"
  @click="goToRideDetailsScreen"
>

  <!-- display either icon if type="own" | "booked" or image if type="other" -->
  <img v-if="props.ride.type === 'other'" :src="props.ride.image" alt="Profilbild" class="profile-picture"/>
  <component v-else-if="props.ride.type === 'own'" :is="Car" class="icon-xl" :class="stateInfo.standardTextClass"/>
  <component v-else :is="Users" class="icon-xl" :class="stateInfo.standardTextClass" />

  <div class="ride-card-content">
    <p class="text-s text-neutral-400">{{ formatDate(props.ride.departure_date) }} | {{ formatTime(props.ride.departure_time) }}</p>
    <div class="car-info-container">
      <p class="text-md" :class="stateInfo.standardTextClass">
          {{ props.ride.end_location.street }}, {{ props.ride.end_location.postal_code }} {{ props.ride.end_location.city }}
      </p>
    </div>

    <!-- Display point cost / reward -->
    <p v-if="props.ride.type === 'other'" class="text-s text-bold">
      {{ props.ride.n_available_seats }} Plätze frei
    </p>
    <p v-else-if="props.ride.type === 'own'" class="text-s text-bold">
      + {{ props.ride.point_reward }} Punkte
    </p>
    <p v-else-if="props.ride.type === 'booked' && props.ride.state === 'accepted'" class="text-s text-bold">
      - {{ props.ride.point_cost }} Punkte
    </p>

    <!-- Display custom message depending on state of the ride -->
    <p v-if="stateInfo.message" class="text-s text-bold" :class="stateInfo.infoTextClass">
      {{ stateInfo.message }}
    </p>

  </div>
  <span v-if="stateInfo.message" class="dot" :class="stateInfo.infoTextClass"/>
</div>
</template>

  
<style scoped>
  .ride-card-container {
    width: 100%;
    background-color: var(--color-neutral-100);
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 20px;
  }
  
  .ride-card-content {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  
  .car-info-container {
    display: flex;
    flex-direction: row;
  }

  .profile-picture {
    width: var(--profile-picture-s-dim); 
    height: var(--profile-picture-s-dim); 
    border-radius: 9999px;
  }

  .selected {
    border-left: var(--line-width-m) solid var(--color-primary-500);
  }

  .dot {
    display: inline-block;
    width: var(--status-dot-size);
    height: var(--status-dot-size);
    padding-right: var(--status-dot-size);
    border-radius: 50%;
    background: currentColor; /* inherits text color */
  }
</style>