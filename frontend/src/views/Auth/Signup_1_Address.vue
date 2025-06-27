<script setup lang="ts">
import axios from 'axios';
import Input from '@/components/Input.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import type { ButtonProps } from '@/types/Props';
import { ref } from 'vue';
import { isValidEmail, isTHBEmail, isValidPassword, required, validate, isValidPostalCode } from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation';
import { useAuth } from '@/composables/useAuth';
import { useUser } from '@/composables/useUser';
import { useToaster } from '@/composables/useToaster';


// composable functions
const { getEmptyUserUpdate } = useUser();
const { registerUser } = useAuth();
const { showDefaultError, showToast } = useToaster();


// variables
const userUpdate = getEmptyUserUpdate()

const userUpdateValidationSchema: ValidationSchema = {
  user_name: [required('Benutzername')],
  first_name: [required('Vorname')],
  last_name: [required('Nachname')],
  email: [required('E-Mail'), isValidEmail(), isTHBEmail()],

  country: [required('Land')],
  postal_code: [required('PLZ'), isValidPostalCode()],
  city: [required('Stadt')],
  street: [required('Straße')],
  house_number: [required('Hausnummer')],
}
const errors = ref<Record<string, string[]>>({})


// functions
const tryRegisterUser = async (): Promise<void> => {
  // validate input
  errors.value = validate(userUpdate, userUpdateValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    console.log(errors.value)
    return
  }
  
  // try to post input data
  try {
    await registerUser(userUpdate)
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      showToast("error", "Fehler beim Registrierungsprozess.")
    } else {
      showDefaultError();
    }
    throw error
  }
}


// components
const hoverButtons: ButtonProps[] = [
  {variant: "primary", text: "Nächster Schritt", onClick: tryRegisterUser},
  {variant: "tertiary", text: "Später", to: "/signup/car"},
]

</script>

<template>
  <div class="view-container">

    <PageTitle>Account einrichten 1/3</PageTitle>

    <h2>Teile uns deine Adresse mit für bequeme Planung deiner ersten Fahrt.</h2>
    <div class="form-container">
      <Input 
        type="text" 
        label="Benutzername" 
        v-model="userUpdate.user_name"
        :error="errors.user_name?.[0]"
      />
      <Input 
        type="text" 
        label="Vorname" 
        v-model="userUpdate.first_name"
        :error="errors.first_name?.[0]"
      />
      <Input 
        type="text" 
        label="Nachname" 
        v-model="userUpdate.last_name"
        :error="errors.last_name?.[0]"
      />
      <Input 
        type="text" 
        label="THB E-Mail" 
        v-model="userUpdate.email"
        :error="errors.email?.[0]"
      />
      <Input 
        type="password" 
        label="Passwort" 
        v-model="userUpdate.password"
        :error="errors.password?.[0]"
        />
      </div>
      
      <HoverButton :buttons="hoverButtons"/>
    </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}

.form-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--horizontal-gap)
}

.error {
  color: var(--color-support-danger-500);
  font-size: var(--font-size-xs);
  margin-bottom: 0.5em;
}
</style>