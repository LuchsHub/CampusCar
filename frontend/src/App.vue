<script setup lang="ts">
import TabBar from '@/components/TabBar.vue'
import { useRoute } from 'vue-router'
const route = useRoute()
import { useKeyboardVisible, isKeyboardVisible } from '@/composables/useKeyboardVisible';
useKeyboardVisible();
</script>

<template>
    <div :class="['app-root', { 'keyboard-visible': isKeyboardVisible }]">
      <router-view />
      <TabBar v-if="!route.meta.hideTabBar && !isKeyboardVisible" />
    </div>
  </template>
  
  <style>
  .app-root {
    /* your default padding */
    max-width: 1280px;
    padding: var(--app-padding-vertical) var(--app-padding-horizontal) calc(var(--nav-min-height) + var(--app-padding-vertical)); 
    position: relative;
    min-height: 100vh;
  }
  .keyboard-visible {
    padding-bottom: 20px !important; /* or 0, or whatever you want */
  }
  </style>
