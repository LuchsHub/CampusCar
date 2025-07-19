<script setup lang="ts">
import Input from '@/components/Input.vue'
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import { ref } from 'vue';

const loading = ref<boolean>(false)
const charges = ref<number>(0)

const onChargeBalance = async () => {
  loading.value = true;
  console.log('charge balance called');
  loading.value = false;
}
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
    <PageTitle :goBack="true">Guthaben aufladen</PageTitle>
    
    <p class="text-md text-bold margin-botton-l">Hier kannst du dein Guthaben aufladen, um später deine Fahrten zu bezahlen.</p>
    <div class="form-container">
      <Input 
        type="number"
        label="Anzahl Sitzplätze (inkl. Fahrer)" 
        v-model="carCreate.n_seats"
        :min="1"
        :max="1000"
        :error="errors.n_seats?.[0]"
        />
    </div>

    <HoverButton :buttons='[
      {variant: "primary", onClick: onChargeBalance, text: "Aufladen", disabled: !!charges, loading: loading}]'
    />
  </div>
</template>

<style scoped>

</style>