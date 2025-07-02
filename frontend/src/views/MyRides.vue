<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import HoverButton from '@/components/HoverButton.vue';
import type { ButtonProps } from '@/types/Props';
import TabSwitcher from '@/components/TabSwitcher.vue';
import { ref } from 'vue';

const activeTab = ref('Bevorstehend')
const tabs = ['Bevorstehend', 'Vergangen']

const hoverButtons: ButtonProps[] = [
    {variant: "primary", text: "Fahrt anbieten", to: "/create_ride"},
]

</script>

<template>
  <div class="view-container">
    <PageTitle>Meine Fahrten</PageTitle>
    <TabSwitcher v-model="activeTab" :tabs="tabs" />
      <div v-if="activeTab === 'Bevorstehend'">
        <h2>Bevorstehend</h2>
      </div>
      <div v-else>
        <h2>Vergangen</h2>
      </div>
    <HoverButton :buttons="hoverButtons"/>
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>