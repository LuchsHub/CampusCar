<script setup lang="ts">
import type { RideCardProps } from '@/types/Props';
import { formatDate, formatTime } from '@/services/utils';

const props = defineProps<RideCardProps & { selected: boolean }>();
const emit = defineEmits(['rideSelected']);

const handleClick = () => {
  emit('rideSelected', props.ride.id);
};
</script>

<template>
  <div class="ride-card-container" :class="{ selected: props.selected }" @click="handleClick">
    <component :is="'Users'" class="icon-xl text-neutral-400" />
    <div class="ride-card-content">
      <p class="text-s text-neutral-400">
        {{ formatDate(props.ride.departure_date) }} | {{ formatTime(props.ride.departure_time) }}
      </p>
      <p class="text-md text-neutral-900">
        {{ props.ride.end_location.street }}, {{ props.ride.end_location.postal_code }} {{ props.ride.end_location.city }}
      </p>
      <p class="text-s text-bold">{{ props.ride.n_available_seats }} Plätze frei</p>
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
.ride-card-container {
  display: flex;
  gap: 20px;
  padding: 1rem 0;
  cursor: pointer;
  border-left: 4px solid transparent;
  transition: all 0.2s ease;
}
.ride-card-container.selected {
  border-left: 4px solid var(--color-primary-500);
  background-color: var(--color-neutral-100);
}
</style>
