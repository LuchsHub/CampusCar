<script setup lang="ts">
import { ref } from 'vue'

const title = ref('Welcome to CampusCar')
</script>

<template>
  <main>
    <h1>{{ title }}</h1>
  </main>
</template>

<style scoped>
main {
  padding: 2rem;
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
}
</style> 