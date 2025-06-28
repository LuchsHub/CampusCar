<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';

const hoverButtons: ButtonProps[] = [
  {variant: "primary", color: "danger", text: "Echsenmenschen?"},
]
</script>

<template>
  <div class="view-container">
    <PageTitle :goBack="true">404</PageTitle>
    <h2>Diese Seite existiert nicht.</h2>
    <p>Oder haben die Echsenmenschen aus der Hohlerde sie verschwinden lassen?</p>
    <a href="https://www.youtube.com/watch?v=xvFZjo5PgG0&list=RDxvFZjo5PgG0&start_radio=1" class="pointer" target="_blank">
      <HoverButton :buttons="hoverButtons"/>
    </a>
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