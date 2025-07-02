<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'

const props = defineProps<{
  modelValue: number
  minY?: number
  maxY?: number
}>()

const emit = defineEmits(['update:modelValue'])

const sheetY = ref(props.modelValue)
const minY = ref(0)
const maxY = ref(0)
let isDragging = false
let startY = 0
let initialY = 0

onMounted(() => {
  const vh = window.innerHeight
  minY.value = props.minY ?? vh * 0.33
  maxY.value = props.maxY ?? vh - 120
  sheetY.value = props.modelValue || maxY.value
})

watch(sheetY, (val) => {
  emit('update:modelValue', val)
})

const startDrag = (e: MouseEvent | TouchEvent) => {
  isDragging = true
  startY = 'touches' in e ? e.touches[0].clientY : e.clientY
  initialY = sheetY.value
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('touchmove', onDrag)
  document.addEventListener('mouseup', endDrag)
  document.addEventListener('touchend', endDrag)
}

const onDrag = (e: MouseEvent | TouchEvent) => {
  if (!isDragging) return
  const currentY = 'touches' in e ? e.touches[0].clientY : e.clientY
  const delta = currentY - startY
  sheetY.value = Math.min(Math.max(minY.value, initialY + delta), maxY.value)
}

const endDrag = () => {
  isDragging = false
  const midpoint = (minY.value + maxY.value) / 2
  sheetY.value = sheetY.value < midpoint ? minY.value : maxY.value
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  document.removeEventListener('touchend', endDrag)
}

onBeforeUnmount(() => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  document.removeEventListener('touchend', endDrag)
})
</script>

<template>
  <div class="bottom-sheet" :style="{ transform: `translateY(${sheetY}px)` }">
    <div class="drag-handle" @mousedown="startDrag" @touchstart="startDrag" />
    <div class="sheet-inner">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.bottom-sheet {
  position: fixed;
  inset-inline: 0;
  margin-inline: auto;
  width: 100%;
  max-width: 768px;
  height: 100%;
  background: white;
  border-top-left-radius: var(--border-radius-l);
  border-top-right-radius: var(--border-radius-l);
  z-index: 10;
  transition: transform 0.2s ease;
  touch-action: none;
  overflow: hidden;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.15);
  will-change: transform;
  bottom: -5px;
  border-radius: 12px;
}

.drag-handle {
  width: 40px;
  height: 5px;
  background-color: var(--color-neutral-300);
  border-radius: 3px;
  margin: 0.75rem auto;
  cursor: grab;
}
.drag-handle:active {
  cursor: grabbing;
}

.sheet-inner {
  height: calc(100% - 40px);
  overflow-y: auto;
  padding: 0 1rem 6rem 1rem;
}
</style>