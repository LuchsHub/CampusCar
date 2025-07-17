<script setup lang="ts">
import Input from '@/components/Input.vue';
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import { ref, reactive } from 'vue';
import { required, validate } from '@/services/validation'
import type { ValidationSchema } from '@/types/Validation';
import router from "@/router";
import { useUser } from '@/composables/useUser';


// composable functions
const { updateUserHasLicense } = useUser()


// variables
const license = reactive({ // mock license
  file: ""
})

const licenseValidationSchema: ValidationSchema = {
  file: [required('Führerschein')],
}
const errors = ref<Record<string, string[]>>({})
const loading = ref(false);


// functions
const tryUploadLicense = async (): Promise<void> => { // this is a mock function. uploading a drivers license is and will not be implemented. 

  errors.value = validate(license, licenseValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    return
  }

  loading.value = true;
  await updateUserHasLicense(true);
  loading.value = false;
  router.push('/home');
}
</script>

<template>
  <div class="view-container">

    <PageTitle :goBack="true">Account einrichten 3/3</PageTitle>

    <p class="text-md text-bold margin-botton-l">Lade ein Bild der Vorder- und Rückseite deines Führerscheins hoch.</p>
    <div class="form-container">
      <div>
        <Input 
        type="file" 
        label="Führerschein" 
        v-model="license.file"
        :error="errors.file?.[0]"
        />
      </div>
    </div>

    <HoverButton :buttons='[
      {variant: "primary", text: "Einrichtung abschließen", onClick: tryUploadLicense, loading: loading},
      {variant: "tertiary", text: "Später", to: "/home"}]'
    />
  </div>
</template>