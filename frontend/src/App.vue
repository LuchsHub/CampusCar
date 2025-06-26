<script setup lang="ts">
import TabBar from './components/TabBar.vue'
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
    <router-view />
    <TabBar v-if="!route.meta.hideTabBar" />
</template>
