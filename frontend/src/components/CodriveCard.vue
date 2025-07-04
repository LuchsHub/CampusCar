<script setup lang="ts">
import type { CodriveCardProps } from '../types/Props'
import { ChevronRight } from 'lucide-vue-next';

const props = defineProps<CodriveCardProps>();
</script>

<template>
<div class="codrive-card-container" :class="{'new-request-container': !props.codrive_accepted}">
    <div class="codrive-card-content">
        <p class="text-neutral-400" :class="{'text-info': !props.codrive_accepted}">Platz {{ props.seat_no }}</p>
        <p v-if="props.codrive_accepted" class="text-md">{{ props.codrive.user.first_name }} {{ props.codrive.user.last_name }}</p>
        <p v-else class="text-md">Anfrage ausstehend </p>
    </div>
    <component v-if="!props.codrive_accepted" :is="ChevronRight" class="icon-md icon-info"/>
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
  