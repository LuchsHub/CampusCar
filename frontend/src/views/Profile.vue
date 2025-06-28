<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';
import { useAuth } from '@/composables/useAuth';
import router from '@/router';

const { logoutUser } = useAuth();

const tryLogoutUser = (): void => {  
  logoutUser();
  router.push('/login');
}

const hoverButtons: ButtonProps[] = [
    {variant: "primary", text: "Logout", color:"danger", onClick:tryLogoutUser},
]

</script>

<template>
  <div class="view-container">
    <PageTitle>Profil</PageTitle>
    <h2>Hier gibts noch nicht viel zu sehen</h2>
    <HoverButton :buttons="hoverButtons"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>