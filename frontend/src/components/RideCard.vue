<template>
  <div class="fahrt-card">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <img :src="ride.image" alt="Profilbild" style="width: 40px; height: 40px; border-radius: 9999px;" />
      <div>
        <p class="fahrt-sub">{{ ride.date }} | Ankunft {{ ride.time }}</p>
        <p class="fahrt-title">{{ ride.to }}</p>
        <p class="fahrt-preis">{{ ride.price }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  ride: {
    id: number
    to: string
    date: string
    time: string
    price: string
    image: string
  }
}>()
</script>

<style scoped>
.fahrt-card {
  border: 1px solid var(--color-primary-200);
  border-radius: var(--border-radius-m);
  padding: 1rem;
  background-color: white;
}

.fahrt-title {
  font-weight: bold;
}

.fahrt-sub {
  font-size: var(--font-size-s);
  color: var(--color-primary-500);
  margin-bottom: 0.25rem;
}

.fahrt-preis {
  color: var(--color-success-500);
  font-weight: bold;
}
</style>
