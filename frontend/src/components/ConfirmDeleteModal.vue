<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  (e: 'cancel'): void
  (e: 'confirm'): void
}>()

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
  <div v-if="props.open" class="modal-backdrop">
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
