<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue'
import Button from '@/components/Button.vue'

// Falls du später zur vorherigen Seite zurück möchtest
import { useRouter } from 'vue-router'
const router = useRouter()

const goBack = () => {
  router.back()
}
</script>

<template>
  <div class="view-container">
    <PageTitle :goBack="true">Auto hinzufügen</PageTitle>

    <div class="under-construction-container">
      <p class="under-construction-text">Diese Seite befindet sich noch im Aufbau 🚧</p>
      <Button variant="primary" @click="goBack">Zurück</Button>
    </div>
  </div>
</template>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  padding: 0 1rem 4rem;
  align-items: center;
}

.under-construction-container {
  margin-top: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.under-construction-image {
  max-width: 300px;
  height: auto;
}

.under-construction-text {
  font-size: 1.25rem;
  color: var(--color-support-info-500);
  text-align: center;
}
</style>
