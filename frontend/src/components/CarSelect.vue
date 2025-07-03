<script setup lang="ts">
import type { CarSelectProps } from '@/types/Props';

const props = defineProps<CarSelectProps>();
const emit = defineEmits(['select']);

</script>

<template>
<div 
  class="car-item-container" 
  :class="{'selected': props.selected}"
  @click="emit('select', props.car)"  
>
  <p class="text-s text-neutral-400">{{ props.car.license_plate }}</p>
  <div class="car-info-container">
    <p 
      class="text-md text-neutral-400"
      :class="{'text-neutral-900': props.selected}">
        {{ props.car.brand }} {{ props.car.model }} | {{ props.car.n_seats }} Sitzplätze
    </p>
  </div>
</div>
</template>

  
<style scoped>
  .car-item-container {
    width: 100%;
    padding: var(--container-padding-vertical) var(--container-padding-horizontal);
    background-color: var(--color-neutral-100);
    display: flex;
    flex-direction: column;
  }
  
  .car-info-container {
    display: flex;
    flex-direction: row;
  }

  .selected {
    border-left: var(--line-width-m) solid var(--color-primary-500);
  }
</style>
  