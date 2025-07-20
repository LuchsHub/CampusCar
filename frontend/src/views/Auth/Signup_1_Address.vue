<script setup lang="ts">
import Input from '@/components/Input.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import { ref } from 'vue';
import { validate } from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation';
import { useLocation } from '@/composables/useLocation';
import router from "@/router";
import { useUser } from '@/composables/useUser';


// composable functions
const { getEmptyLocationCreate, getLocationCreateValidationSchema } = useLocation();
const { updateUserLocation } = useUser();


// variables
const locationCreate = getEmptyLocationCreate()
const locationCreateValidationSchema: ValidationSchema = getLocationCreateValidationSchema();
const errors = ref<Record<string, string[]>>({})
const loading = ref<boolean>(false);


// functions
const tryUpdateUserLocation = async (): Promise<void> => {

  errors.value = validate(locationCreate as Record<string, string>, locationCreateValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    return
  }

  loading.value = true;
  await updateUserLocation(locationCreate);
  loading.value = false;
  router.push('/signup/car');
}
</script>

<template>
  <div class="view-container">

    <PageTitle>Account einrichten 1/3</PageTitle>

    <p class="text-md text-bold margin-botton-l">Teile uns deine Adresse mit - für die bequeme Planung deiner ersten Fahrt.</p>
    <div class="form-container">
      <Input 
        type="text" 
        label="Land" 
        v-model="locationCreate.country"
        :error="errors.country?.[0]"
      />
      <Input 
        type="text" 
        label="Straße" 
        v-model="locationCreate.street"
        :error="errors.street?.[0]"
      />
      <Input 
        type="text"
        label="Hausnummer" 
        v-model="locationCreate.house_number"
        :error="errors.house_number?.[0]"
        />
      <Input 
        type="text" 
        label="Stadt" 
        v-model="locationCreate.city"
        :error="errors.city?.[0]"
      />
      <Input 
        type="number" 
        label="PLZ" 
        v-model="locationCreate.postal_code"
        :error="errors.postal_code?.[0]"
        :maxLength="5"
      />
      </div>
      
      <HoverButton :buttons='[
        {variant: "primary", text: "Nächster Schritt", onClick: tryUpdateUserLocation, loading: loading},
        {variant: "tertiary", text: "Später", to: "/signup/car"}]'
      />
    </div>
</template>