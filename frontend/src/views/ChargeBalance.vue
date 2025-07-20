<script setup lang="ts">
import Input from '@/components/Input.vue'
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import { onMounted, ref } from 'vue';
import { useUser } from '@/composables/useUser';
import type { ValidationSchema } from '@/types/Validation';
import { smallerThan, largerThan, required, validate } from '@/services/validation';
import { useToaster } from '@/composables/useToaster';
import { useRouter } from 'vue-router';

const { getUserBalance, chargeUserBalance } = useUser(); 
const { showToast } = useToaster();

const router = useRouter();

const loading = ref<boolean>(false);
const amount = ref<number | string>(0);
const balance = ref<number>(0);

const chargeBalanceValidationSchema: ValidationSchema = {
  amount: [required('Betrag'), largerThan(0, 'Beträge zwischen 1 - 1000€ möglich.'), smallerThan(1001, 'Beträge zwischen 1 - 1000€ möglich.')]
}

const errors = ref<Record<string, string[]>>({})

onMounted(async() => {
  balance.value = await getUserBalance();
})

const onChargeBalance = async () => {
  errors.value = validate({'amount': amount.value} as Record<string, string>, chargeBalanceValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    return
  }

  try {
    loading.value = true;
    const newBalance = await chargeUserBalance(Number(amount.value));
    showToast('success', `Neues Guthaben: ${newBalance}€`);
    balance.value = newBalance;
    amount.value = 0;
    router.go(-1);
  } catch (error:unknown) {
    console.log(error);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
    <PageTitle :goBack="true">Guthaben aufladen</PageTitle>
    
    <h2 class="margin-botton-l margin-top-l center-text">Aktuelles Guthaben:</h2>
    
    <p class="text-xxl text-semibold text-primary margin-bottom-xxl center-text">{{ balance.toFixed(2) }}€</p>

    <div class="form-container">
      <Input 
        type="number"
        label="Aufzuladener Betrag (€)" 
        v-model="amount"
        :min="1"
        :max="1001"
        :error="errors.amount?.[0]"
        />
    </div>

    <HoverButton :buttons='[
      {variant: "primary", onClick: onChargeBalance, text: "Aufladen", disabled: amount===0, loading: loading}]'
    />
  </div>
</template>