<script setup lang="ts">
import type { BonusCardProps } from '../types/Props'

const props = defineProps<BonusCardProps>();
</script>

<template>
<div
    class="bonus-card"
    :class="{ selected: props.selected }"
    @click="$emit('click')"
>
    <p class="text-l text-semibold">{{ props.bonus.name }}</p>
    <p v-if="!props.isRedeemed" class="text-md"><span class="text-semibold">{{ props.bonus.cost }} </span> Punkte</p>
    <p v-else class="text-md"><span class="text-semibold">{{ props.bonus.count }} </span>x</p>
</div>
</template>

<style scoped>
.bonus-card {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    background-color: var(--color-neutral-100);
    border: var(--line-width-m) solid var(--color-neutral-300);
    width: 100%;
    border-radius: var(--border-radius);
    padding: 25px 30px
}

.bonus-card.selected {
    border: var(--line-width-m) solid var(--color-primary-500);
    box-shadow: 0 1px 10px var(--color-primary-500-transparent);
}
</style>
  