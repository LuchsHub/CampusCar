<script setup lang="ts">
import { useRoute } from 'vue-router'
import { Home, Car, User } from 'lucide-vue-next'
import type { TabItem } from '../types/TabItem'

const route = useRoute()

const items: TabItem[] = [
  { label: 'Home', to: '/', icon: Home },
  { label: 'Beispiel', to: '/example', icon: Car },
  { label: 'Styles', to: '/styles', icon: User }
]

const isActive = (path: string): boolean => route.path === path
</script>

<template>
  <nav>
    <RouterLink
      v-for="item in items"
      :key="item.label"
      :to="item.to"
      class="text-xs text-bold text-neutral-300"
      :class="{ 'text-neutral-900': isActive(item.to) }"
    >
      <component :is="item.icon" class="icon-xl" />
      {{ item.label }}
    </RouterLink>
  </nav>
</template>

<style scoped>
nav {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;   
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  min-height: var(--nav-min-height);
  width: 100%;
  box-shadow: 0 -1px 10px var(--color-neutral-900-transparent);
  background-color: var(--color-neutral-100);
}

a {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
</style>
