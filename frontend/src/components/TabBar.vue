<script setup lang="ts">
import { useRoute } from 'vue-router'
import { Home, Car, User } from 'lucide-vue-next'
import type { TabItem } from '../types/TabItem'

const route = useRoute()

const items: TabItem[] = [
  { label: 'Home', to: '/home', icon: Home },
  { label: 'Fahrten', to: '/my_rides', icon: Car },
  { label: 'Profil', to: '/profile', icon: User }
]

const isActive = (path: string): boolean => route.path === path
</script>

<template>
  <nav>
    <div class="icon-container">
      <RouterLink
        v-for="item in items"
        :key="item.label"
        :to="item.to"
        class="text-xs text-bold text-neutral-300"
        :class="{ 'text-neutral-900': isActive(item.to) }"
      >
        <component :is="item.icon" class="icon-md" />
        {{ item.label }}
      </RouterLink>
    </div>
  </nav>
</template>

<style scoped>
nav {
  position: fixed;
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  left: 0;
  right: 0;
  bottom: 0;   
  box-shadow: 0 -1px 10px var(--color-neutral-900-transparent);
  background-color: var(--color-neutral-100);
}

.icon-container {
  width: 100%;
  min-height: var(--nav-min-height);
  display: flex;
  justify-content: space-around;
  align-items: center;
  flex-direction: row;
}

@media (min-width: 768px) {
  .icon-container {
    max-width: var(--tablet-content-max-width);
  }
}

@media (min-width: 1200px) {
  .icon-container {
    max-width: var(--desktop-content-max-width);
  }
}

a {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
</style>
