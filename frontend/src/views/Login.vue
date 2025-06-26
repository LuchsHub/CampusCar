<script setup lang="ts">
import Input from '../components/Input.vue';
import Button from '../components/Button.vue';
import HoverButton from '../components/HoverButton.vue';
import PageTitle from '../components/PageTitle.vue';
import type { ButtonProps } from '../types/Props';
import type { UserLogin } from '../types/User';
import { reactive, ref } from 'vue';
import { required } from '../services/validation'
import type { ValidationSchema } from '../types/Validation';

const userLogin = reactive<UserLogin>({
  email: "",
  password: "",
})

const errors = ref<Record<string, string[]>>({})

const userValidationSchema: ValidationSchema = {
  email: [required('E-Mail ist erforderlich')],
  password: [required('Passwort ist erforderlich')],
}

const hoverButtons: ButtonProps[] = [
  {variant: "primary", text: "Anmelden", onClick: ()=>{}},
  {variant: "tertiary", text: "Account erstellen", onClick: ()=>{}},
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