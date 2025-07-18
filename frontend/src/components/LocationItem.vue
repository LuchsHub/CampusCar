<script setup lang="ts">
import type { LocationItemProps } from '@/types/Props';
import { formatTime, formatDate } from '@/services/utils';
import { User } from 'lucide-vue-next';

const props = defineProps<LocationItemProps>();
</script>

<template>
<div class="location-item-container">
    
    <div class="date-info-container">
        <p v-if="props.arrival_date" class="text-xs text-neutral-400">{{ formatDate(props.arrival_date) }}</p>
        <div class="time-container">
            <p class="text-l text-bold" :class="{'text-strikethrough text-neutral-400': props.updated_arrival_time}">{{ formatTime(props.arrival_time) }}</p>
            <p v-if="props.updated_arrival_time" class="text-l text-bold text-danger">{{ formatTime(props.updated_arrival_time) }}</p>
        </div>
    </div>

    <div class="location-item-content">
        <p class="text-md">{{ props.location.street }} {{ props.location.house_number }}</p>
        <p class="text-md">{{ props.location.postal_code }} {{ props.location.city }}</p>
        <div v-if="props.user" class="user-container">
            <component :is="User" class="icon-xs"/>
            <p class="text-md text-bold">{{ props.user.first_name }} {{ props.user.last_name }}</p>
        </div>
    </div>
</div>
</template>

  
<style scoped>
.location-item-container {
    width: 100%;
    background-color: var(--color-neutral-100);
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 20px;
}

.date-info-container {
    height: 100%;
    width: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 6px;
}

.time-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.location-item-content {
    width: 100%;
    border-left: var(--line-width-s) solid var(--color-neutral-900);
    padding: 4px 0 4px 20px;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.user-container {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 7px;
    margin-top: 4px;
}
</style>