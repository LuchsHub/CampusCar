<script setup lang="ts">
import type { InformationItemProps } from '@/types/Props';
import { UserPlus, Users, DollarSign, Info, MessageCircle } from 'lucide-vue-next';
import { computed } from 'vue';

const props = defineProps<InformationItemProps>();

const stateInfo = computed(() => {
  switch (props.type) {
    case 'availableSeats':
        return {'icon': Users, 'text': 'Freie Plätze'}
    case 'bookedSeats':
        return {'icon': UserPlus, 'text': 'Gebuchte Plätze'}
    case 'pointReward':
        return {'icon': DollarSign, 'text': 'Vergütung', 'unit': 'Punkte'}
    case 'pointCost':
        return {'icon': DollarSign, 'text': 'Kosten', 'unit': 'Punkte'}
    case 'message':
        return {'icon': MessageCircle, 'text': 'Nachricht'}
    default:
        return {'icon': Info}
  }
})
</script>

<template>
<div class="information-item-container">
    <component :is="stateInfo.icon" class="icon-l"/>
    <div class="info-container">
        <p class="text-s text-neutral-400">{{ stateInfo.text }}</p>
        <p class="text-l text-bold">{{ props.value }} {{ stateInfo.unit }}</p>
    </div>
</div>
</template>

  
<style scoped>
.information-item-container {
    width: 100%;
    background-color: var(--color-neutral-100);
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 20px;
}

.info-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 2px;
}
</style>