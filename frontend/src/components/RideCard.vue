<script setup lang="ts">
import type { RideCardProps } from '@/types/Props';
import { computed } from 'vue';

const props = defineProps<RideCardProps>();
import { Users } from 'lucide-vue-next';

function formatDateTime(date: string, time: string): string {
  const [year, month, day] = date.split('-');
  const [hour, minute] = time.split(':');
  return `${day}.${month}.${year.slice(2)} | ${hour}:${minute}`;
}

const stateInfo = computed(() => {
  switch (props.state) {
    case 'new request':
      return { message: 'Neue Anfrage', infoTextClass: 'text-info', standardTextClass: 'text-neutral-900'}
    case 'not accepted':
      return { message: 'Noch nicht akzeptiert', infoTextClass: 'text-warning' , standardTextClass: 'text-neutral-400'}
    case 'rejected':
      return { message: 'Abgelehnt', infoTextClass: 'text-danger', standardTextClass: 'text-neutral-400 text-strikethrough'}
    case 'accepted':
      return { message: 'Angenommen', infoTextClass: 'text-success', standardTextClass: 'text-neutral-900'}
    default:
      return { message: '', infoTextClass: '' }
  }
})
</script>

<template>
<div class="ride-card-container">
  <component :is="Users" class="icon-xl" :class="stateInfo.standardTextClass" />
  <div class="ride-card-content">
    <p class="text-s text-neutral-400">{{formatDateTime(props.ride.departure_date, props.ride.departure_time)}}</p>
    <div class="car-info-container">
      <p class="text-md text-semibold" :class="stateInfo.standardTextClass">
          {{ props.ride.end_location.street }}, {{ props.ride.end_location.postal_code }} {{ props.ride.end_location.city }}
      </p>
    </div>
    <p 
      v-if="stateInfo.message" 
      class="text-s text-bold"
      :class="stateInfo.infoTextClass"
    >
      {{ stateInfo.message }}
    </p>
  </div>
  <span v-if="stateInfo.message" class="dot" :class="stateInfo.infoTextClass"></span>
</div>
</template>

  
<style scoped>
  .ride-card-container {
    width: 100%;
    padding: var(--container-padding-vertical) var(--container-padding-horizontal);
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
  