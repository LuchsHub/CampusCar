<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';

const hoverButtons: ButtonProps[] = [
    {variant: "primary", text: "Fahrt anbieten", to: "/create_ride"},
]

</script>

<template>
  <div class="view-container">
    <PageTitle>Meine Fahrten</PageTitle>
    <h2>Hier gibts noch nicht viel zu sehen</h2>
    <HoverButton :buttons="hoverButtons"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>