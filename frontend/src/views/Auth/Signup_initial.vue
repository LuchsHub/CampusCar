<script setup lang="ts">
import axios from 'axios';
import Input from '@/components/Input.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import type { ButtonProps } from '@/types/Props';
import { ref } from 'vue';
import { isValidEmail, isTHBEmail, isValidPassword, required, validate } from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation';
import { useAuth } from '@/composables/useAuth';
import { useUser } from '@/composables/useUser';
import { useToaster } from '@/composables/useToaster';


// composable functions
const { getEmptyUserRegister } = useUser();
const { registerUser } = useAuth();
const { showDefaultError, showToast } = useToaster();


// variables
const userRegister = getEmptyUserRegister()

const userRegisterValidationSchema: ValidationSchema = {
  user_name: [required('Benutzername')],
  first_name: [required('Vorname')],
  last_name: [required('Nachname')],
  email: [required('E-Mail'), isValidEmail(), isTHBEmail()],
  password: [required('Passwort'), isValidPassword()],
}
const errors = ref<Record<string, string[]>>({})


// functions
const tryRegisterUser = async (): Promise<void> => {
  // validate input
  errors.value = validate(userRegister, userRegisterValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    console.log(errors.value)
    return
  }
  
  // try to post input data
  try {
    await registerUser(userRegister)
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
  {variant: "primary", text: "Registrieren", onClick: tryRegisterUser},
  {variant: "tertiary", text: "Ich habe schon einen Account", to: "/login"},
]

</script>

<template>
  <div class="view-container">

    <PageTitle>Registrieren</PageTitle>

    <h2>Erstelle einen Account, um direkt loszulegen!</h2>
    <div class="form-container">
      <Input 
        type="text" 
        label="Benutzername" 
        v-model="userRegister.user_name"
        :error="errors.user_name?.[0]"
      />
      <Input 
        type="text" 
        label="Vorname" 
        v-model="userRegister.first_name"
        :error="errors.first_name?.[0]"
      />
      <Input 
        type="text" 
        label="Nachname" 
        v-model="userRegister.last_name"
        :error="errors.last_name?.[0]"
      />
      <Input 
        type="text" 
        label="THB E-Mail" 
        v-model="userRegister.email"
        :error="errors.email?.[0]"
      />
      <Input 
        type="password" 
        label="Passwort" 
        v-model="userRegister.password"
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
</style>