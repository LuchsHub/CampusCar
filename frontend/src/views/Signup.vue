<script setup lang="ts">
import Input from '../components/Input.vue';
import HoverButton from '../components/HoverButton.vue';
import PageTitle from '../components/PageTitle.vue';
import type { ButtonProps } from '../types/Props';
import type { UserRegister } from '../types/User';
import { reactive, ref } from 'vue';
import { isValidEmail, isTHBEmail, isValidPassword, required, validate } from '../services/validation'
import type { ValidationSchema } from '../types/Validation';
import { useAuth } from '../composables/useAuth';
import { useToaster } from '../composables/useToaster';
import axios from 'axios';

const userRegister = reactive<UserRegister>({
  email: "",
  password: "",
  full_name: "",
})

const errors = ref<Record<string, string[]>>({})

const userRegisterValidationSchema: ValidationSchema = {
  email: [required('E-Mail ist erforderlich'), isValidEmail(), isTHBEmail()],
  password: [required('Passwort ist erforderlich'), isValidPassword()],
  full_name: [required('Vor- und Nachname ist erforderlich')],
}

const { registerUser } = useAuth();
const { showDefaultError, showToast } = useToaster();

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
        label="Vor- und Nachname" 
        v-model="userRegister.full_name"
        :error="errors.full_name?.[0]"
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