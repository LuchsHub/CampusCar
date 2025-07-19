<script setup lang="ts">
import type { CodriveCardProps } from '../types/Props'
import { ChevronRight } from 'lucide-vue-next';
import router from '@/router';
import { useMyRideStore } from '@/stores/MyRideStore';
import { useToaster } from '@/composables/useToaster';

const props = defineProps<CodriveCardProps>();
const myRideStore = useMyRideStore();
const { showToast } = useToaster();

const goToMyRideCodriverScreen = async () => {
  if (!props.codrive && !props.requested_codrive) {
    return;
  }

  if (!props.requested_codrive) {
    showToast('error', 'Angefragte Mitfahrt nicht verfügbar.');
    return;
  }

  await myRideStore.setRequestedCodrive(props.requested_codrive);
  router.push({ name: 'myRideCodriver' });
}
</script>

<template>
<div 
  class="codrive-card-container" 
  :class="{'new-request-container': props.requested_codrive}"
  @click="goToMyRideCodriverScreen"
>
    <div class="codrive-card-content">
        <p class="text-neutral-400" :class="{'text-info': props.requested_codrive}">Platz {{ props.seat_no }}</p>
        <p v-if="props.codrive" class="text-md">{{ props.codrive.user.first_name }} {{ props.codrive?.user.last_name }}</p>
        <p v-else-if="props.requested_codrive" class="text-md">Anfrage ausstehend </p>
        <p v-else class="text-md">-</p>
    </div>
    <component v-if="props.requested_codrive" :is="ChevronRight" class="icon-md icon-info"/>
</div>
</template>

  
<style scoped>
  .codrive-card-container {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: var(--container-padding-vertical) var(--container-padding-horizontal);
    border-radius: var(--border-radius);
    background-color: var(--color-neutral-200);
  }

  .codrive-card-content {
    width: 100%;
    gap: 8px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
  }

  .new-request-container{
    border: var(--line-width-m) solid var(--color-support-info-500);
  }
</style>
  