<script setup lang="ts">
    import { ChevronLeft } from 'lucide-vue-next'
    import type { PageTitleProps } from '../types/Props'
    import { useRouter } from 'vue-router'

    const props = defineProps<PageTitleProps>()
    const router = useRouter()

    const goBack = () => {
        if (props.goBack) {
            router.go(-1)
        }
    }
</script>

<template>
    <div class="page-title-container">
        <button 
            v-if="props.goBack"
            @click="goBack"
            class="back-button"
        >
            <ChevronLeft class="icon-xl"/>
        </button>
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

.back-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>