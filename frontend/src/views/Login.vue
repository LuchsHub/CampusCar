<script setup lang="ts">
import axios from 'axios';
import Input from '../components/Input.vue';
import HoverButton from '../components/HoverButton.vue';
import PageTitle from '../components/PageTitle.vue';
import type { ButtonProps } from '../types/Props';
import { ref } from 'vue';
import { isValidEmail, required, validate } from '../services/validation'
import type { ValidationSchema } from '../types/Validation';
import { useAuth } from '../composables/useAuth';
import { useToaster } from '../composables/useToaster';
import { useUser } from '../composables/useUser';


// composable functions
const { loginUser } = useAuth();
const { showToast, showDefaultError } = useToaster();
const { getEmptyLoginUser } = useUser();


// variables
const userLogin = getEmptyLoginUser();

const userLoginValidationSchema: ValidationSchema = {
  email: [required('E-Mail ist erforderlich'), isValidEmail()],
  password: [required('Passwort ist erforderlich')],
}
const errors = ref<Record<string, string[]>>({});


// functions
const tryLoginUser = async (): Promise<void> => {
  // validate input
  errors.value = validate(userLogin, userLoginValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    console.log(errors.value)
    return
  }
  
  // try to post input data
  try {
    await loginUser(userLogin)
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      showToast("error", "Ungültige Anmeldedaten.")
    } else {
      showDefaultError();
    }
    throw error
  }
}

// Hoverbuttons
const hoverButtons: ButtonProps[] = [
  {variant: "primary", text: "Anmelden", onClick: tryLoginUser},
  {variant: "tertiary", text: "Account erstellen", to: "/signup"},
]
</script>

<template>
  <div class="view-container">

    <PageTitle>Login</PageTitle>

    <h2>Willkommen zurück!</h2>
    <div class="form-container">
      <Input 
        type="text" 
        label="THB E-Mail" 
        v-model="userLogin.email"
        :error="errors.email?.[0]"
      />
      <Input 
        type="password" 
        label="Passwort" 
        v-model="userLogin.password"
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