<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/AuthStore';

const router = useRouter();
const authStore = useAuthStore();

const hoverButtons: ButtonProps[] = [
  {variant: "primary", text: authStore.userAuthenticated ? 'Zur Startseite' : 'Zum Login'},
]

const navigateToDifferentPage = () => {
  if (authStore.userAuthenticated) {
    router.push('/home');
  } else {
    router.push('/login');
  }
}
</script>

<template>
  <div class="view-container">
    <PageTitle :goBack="true">404</PageTitle>
    <h2>Diese Seite existiert nicht.</h2>
    <HoverButton :buttons="hoverButtons" :onclick="navigateToDifferentPage"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}

.pointer:hover{
  cursor: pointer;
}
</style>