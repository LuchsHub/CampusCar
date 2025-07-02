<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['cancel', 'confirm'])

const input = ref('')

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
  <div v-if="open" class="modal-backdrop">
    <div class="modal-container">
      <h2 class="modal-title">Konto löschen</h2>
      <p class="modal-text">
        Bist du sicher, dass du dein Konto löschen möchtest?<br />
        Gib bitte <strong>„löschen“</strong> ein, um fortzufahren.
      </p>

      <div class="modal-input-wrapper">
        <input
          v-model="input"
          type="text"
          placeholder='Tippe "löschen"'
          class="modal-input"
        />
      </div>

      <div class="modal-actions">
        <button class="btn btn-tertiary" @click="onCancel">Abbrechen</button>
        <button class="btn btn-primary" :disabled="input !== 'löschen'" @click="onConfirm">
          Löschen
        </button>
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
  background-color: white;
  border-radius: 1rem;
  padding: 2rem 1.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-support-danger-500);
  margin-bottom: 1rem;
}

.modal-text {
  font-size: 1rem;
  color: var(--color-neutral-800);
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.modal-input-wrapper {
  display: flex;
  align-items: center;
  background-color: var(--color-background-50, #f8f6f9);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-lg, 12px);
  box-shadow: var(--shadow-xs, 0 1px 2px rgba(0,0,0,0.05));
  margin-bottom: 1.5rem;
}

.modal-input {
  border: none;
  background: transparent;
  outline: none;
  width: 100%;
  font-size: 1rem;
  color: var(--color-text-strong, #1e1b26);
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
}

.btn {
  flex: 1;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s ease;
  border: none;
}

.btn-primary {
  background-color: var(--color-support-danger-500);
  color: white;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-tertiary {
  background-color: var(--color-neutral-200);
  color: var(--color-neutral-900);
}
</style>