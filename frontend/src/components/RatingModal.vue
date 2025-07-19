<script setup lang="ts">
import { ref } from 'vue'
import Button from './Button.vue'
import { Star } from 'lucide-vue-next'


defineProps<{
  open: boolean
}>()

const emit = defineEmits(['cancel', 'confirm'])
const onCancel = () => {
  emit('cancel');
}
const onConfirm = () => {
  emit('confirm', rating.value);
}

const rating = ref(0)

const setRating = (value: number) => {
  rating.value = value
}

// Gibt ein Array mit 5 Einträgen zurück, je nachdem ob der Stern gefüllt ist oder nicht
const getStarIcons = () => {
  return Array.from({ length: 5 }, (_, i) => ({
    filled: i < rating.value
  }))
}
</script>

<template>
  <div v-if="open" class="modal-backdrop">
    <div class="modal-container">
      <p class="text-xl text-semibold margin-botton-l">Bewertung</p>
      <p class="text-md margin-bottom-xl">
        Wie war deine Erfahrung mit Name?
      </p>

      <div class="star-row margin-bottom-xl">
        <component
          v-for="(star, index) in getStarIcons()"
          :key="index"
          :is="Star"
          class="star-icon icon-xl"
          :style="{ fill: star.filled ? 'var(--color-primary-500)' : 'none', stroke: 'var(--color-primary-500)', cursor: 'pointer' }"
          @click="setRating(index + 1)"
        />
      </div>

      <div class="modal-actions">
        <Button variant="primary" :onClick=onConfirm>Bezahlen</Button>
        <Button variant="tertiary" :onClick=onCancel>Abbrechen</Button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.modal-container {
  background-color: var(--color-neutral-100);
  border-radius: var(--border-radius);
  padding: 2rem 1.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.star-row {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}
.star-icon {
  width: 2rem;
  height: 2rem;
  transition: fill 0.2s;
}

.modal-actions {
  display: flex;
  flex-direction: column;
}
</style>