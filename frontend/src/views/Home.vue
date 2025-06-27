<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';
import { useAuth } from '@/composables/useAuth';

const { logoutUser } = useAuth();

const hoverButtons: ButtonProps[] = [
    {variant: "primary", text: "Logout", color:"danger", onClick:logoutUser},
]
</script>

<template>
  <div class="view-container">
    <PageTitle>Home</PageTitle>
    <h2>Hier gibts noch nicht viel zu sehen</h2>
    <p>Theoretisch soll das aber die Seite sein, wo die Kartenansicht zu sehen ist und die aktuellen Fahrten angezeigt werden.</p>
    <HoverButton :buttons="hoverButtons"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>