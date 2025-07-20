<script setup lang="ts">
import { ref } from 'vue'
import Button from './Button.vue'
import type { ConfirmDeleteModalProps } from '@/types/Props';

const props = defineProps<ConfirmDeleteModalProps>()

const emit = defineEmits(['cancel', 'confirm'])

const input = ref<string>('')

const onCancel = () => {
  input.value = ''
  emit('cancel')
}

const onConfirm = () => {
  input.value = ''
  emit('confirm')
}
</script>

<template>
  <div v-if="props.open" class="modal-backdrop">
    <div class="modal-container">
      <p class="text-xl text-semibold margin-botton-l">{{ props.subject }} {{ ["Mitfahrt"].includes(props.subject) ? "absagen" : "löschen" }}</p>
      <p class="text-md margin-bottom-xl">
        Bist du sicher, dass du {{ ["Fahrt", "Mitfahrt"].includes(props.subject) ? "deine" : "dein" }} {{ props.subject }} {{ ["Mitfahrt"].includes(props.subject) ? "absagen" : "löschen" }} möchtest?<br />
        <span v-if="props.requiresTextConfirmation">Gib bitte <span class="text-semibold">„löschen“</span> ein, um fortzufahren.</span>
      </p>

      <div v-if="props.requiresTextConfirmation" class="modal-input-wrapper margin-bottom-xl">
        <input
          v-model="input"
          type="text"
          placeholder='Tippe "löschen"'
          class="modal-input"
        />
      </div>

      <div class="modal-actions">
        <Button variant="primary" color="danger" :disabled="props.requiresTextConfirmation && input !== 'löschen'" :onClick=onConfirm>{{ ["Mitfahrt"].includes(props.subject) ? "Absagen" : "löschen" }}</Button>
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

.modal-input-wrapper {
  display: flex;
  align-items: center;
  background-color: var(--color-neutral-200);
  padding: var(--container-padding-vertical) var(--container-padding-horizontal);
  border-radius: var(--border-radius);
}

.modal-input {
  border: none;
  background: transparent;
  outline: none;
  width: 100%;
  font-size: var(--font-size-md);
  color: var(--color-neutral-900);
  font-weight: var(--font-weight-normal);
}

.modal-actions {
  display: flex;
  flex-direction: column;
  gap: var(--horizontal-gap);
}
</style>