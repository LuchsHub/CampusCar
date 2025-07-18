<script setup lang="ts">
import Input from '@/components/Input.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import { ref } from 'vue';
import { isValidEmail, required, validate } from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation';
import { useAuth } from '@/composables/useAuth';
import { useUser } from '@/composables/useUser';
import router from '@/router';


// composable functions
const { loginUser } = useAuth();
const { getEmptyUserLogin } = useUser();
const loading = ref(false);

// variables
const userLogin = getEmptyUserLogin();

const userLoginValidationSchema: ValidationSchema = {
  email: [required('E-Mail'), isValidEmail()],
  password: [required('Passwort')],
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

  loading.value = true;
  await loginUser(userLogin);
  loading.value = false;
  router.push('/home');
}
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
      
    <HoverButton :buttons="[
      {variant: 'primary', text: 'Anmelden', onClick: tryLoginUser, loading: loading},
      {variant: 'tertiary', text: 'Account erstellen', to: '/signup'}]"
    />
  </div>
</template>

<style scoped>
.view-container h2:first-of-type {
  margin-top: 0;
}
</style>