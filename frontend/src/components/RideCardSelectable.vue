<script setup lang="ts">
import type { RideCardProps } from '@/types/Props';

const props = defineProps<RideCardProps>();
const emit = defineEmits(['rideSelected']);

// wird vom Elternkomponente verwaltet
const handleClick = () => {
  emit('rideSelected', props.ride.id); // signalisiert Klick
};
</script>

<template>
  <div class="ride-card-container" @click="handleClick">
    <component :is="'Users'" class="icon-xl text-neutral-400" />
    <div class="ride-card-content">
      <p class="text-s text-neutral-400">{{ ride.departure_date }} | {{ ride.departure_time }}</p>
      <p class="text-md text-neutral-900">
        {{ ride.end_location.street }}, {{ ride.end_location.postal_code }} {{ ride.end_location.city }}
      </p>
      <p class="text-s text-bold">{{ ride.n_available_seats }} Plätze frei</p>
    </div>
  </div>
</template>

<style scoped>
.ride-card-container {
  display: flex;
  gap: 20px;
  padding: 1rem 0;
  cursor: pointer;
}
.ride-card-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
</style>
