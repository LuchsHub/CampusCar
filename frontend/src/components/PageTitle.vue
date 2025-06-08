<script setup lang="ts">
    import { ChevronLeft } from 'lucide-vue-next'
    import type { PageTitleProps } from '../types/Props'

    const props = defineProps<PageTitleProps>()
</script>

<template>
    <div class="page-title-container">
        <router-link 
            v-if="props.to"
            :to="props.to"
        >
            <ChevronLeft class="icon-xl"/>
        </router-link>
        <h1><slot/></h1>
    </div>
</template>

<style scoped>
.page-title-container {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--page-title-back-arrow-gap);
    margin-bottom: var(--page-title-margin-bottom)
}
</style>