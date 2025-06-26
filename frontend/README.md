# CampusCar Frontend

This is the frontend application for the CampusCar project, built with Vue 3, TypeScript, and Vite.

## Project Structure

```
src/
├── assets/        # Static assets like images and **global styles**
├── components/    # Reusable Vue components
├── composables/   # Like services but for extracting stateful logic (using ref, computed, etc.)
├── layouts/       # Layout components
├── router/        # Vue Router configuration
├── services/      # For extracting stateless logic from components
├── stores/        # State management
├── types/         # TypeScript type definitions
├── utils/         # Utility functions
└── views/         # Page components
```

## Development

Frontend development happens on the branch `frontend_dev`. If you want to add a feature, create a **new branch** based on this branch and PR when finished. New branches follow the following naming conventions: `feature/<issue_no>_<feature_name>`. For example: `feature/5_login_view`.

### Project setup

Install dependencies first:

```bash
cd fronted 
npm install
```

Then start frontend in development mode:

```bash
npm run dev
```

And then start the backend: (**NOTE**: May require `docker login` to work. This will also start the `frontend-1`-container, which sits on the same port as the frontend after starting it with `npm run dev`. If you have trouble with code changes being not displayed, stop the `frontend-1`-container. Should be easily fixable by configurating the ports properly though.)

```bash
docker compose watch
```

After that, the API documentation is available under `http://localhost:8000/docs` and a tool for the database is available here `http://localhost:8080/` (Database credentials: **System**: _PostgreSQL_, **Server**: _db_, **Username**: _postgres_, **Password**: _postgres_)

When you start the application you will only see the login / signup screen. Just create a new user and authenticate to see the rest of the application.

### View structure

Every View should be placed in the `./views` directory. Views follow the following structure, make sure to add class "view-container" to the parent div. 

```html
<template>
  <div class="view-container">
    <PageTitle>Name of the page</PageTitle>
    <HoverButton :buttons="hoverButtons"/> <!--optional-->
  </div>
</template>
```


### Components

Components go in the `./components` directory. Make sure to use global styles for basic stuff like fonts, colors, margin, padding, etc. Those can be found in [the global css file](./src/assets/main.css). Most of the components should not have a fixed width but use `width: 100%` to work responsively. 


### Services

Services go in the `./services` directory. They encapsulate stateless business logic. 

We have 2 Services at the moment: `api.ts` and `validation.ts`:

`api.ts` is for providing a centralized axios instance, you can use it for api calls like in the example below. I think for the protected routes we should implement an interceptor to provice the access token, i mentioned it [here](./src/services/api.ts). The base URL is set in `src/services/api.ts` and can be configured via the `VITE_API_BASE_URL` environment variable.

```typescript
import api from '../services/api'
const response = await api.post(
    '/users/signup',
    user
  )
```

`.validation.ts` is a service for validating form inputs. You can add a validation ruleset for an object like this: (You can add custom rules [here](./src/services/validation.ts))

```typescript
import type { User } from '../types/User';
import { isValidEmail, isTHBEmail, isValidPassword, required } from '../services/validation'
import type { ValidationSchema } from '../types/Validation';

const user = reactive<User>({
  email: "",
  password: "",
})

const userRegisterValidationSchema: ValidationSchema = {
  email: [required('E-Mail ist erforderlich'), isValidEmail(), isTHBEmail()],
  password: [required('Passwort ist erforderlich'), isValidPassword()],
}
```

**IMPORTANT:** When adding a ruleset it is **required** that the keys (e.g. `email`, `password`) are the same as in the object you want to validate. Otherwise validation wont work. 

And validate the current input values like this:

```typescript
import {  validate } from '../services/validation'

const errors = ref<Record<string, string[]>>({})

errors.value = validate(userRegister, userRegisterValidationSchema)
  if (Object.keys(errors.value).length > 0) {
    console.log(errors.value)
    return
  }
```

Make sure to pass the error objects to the Input component to display the error message.

```html
<Input 
  type="text" 
  label="THB E-Mail" 
  v-model="user.email"
  :error="errors.email?.[0]" <!--Error goes here-->
/>
<Input 
  type="password" 
  label="Passwort" 
  v-model="user.password"
  :error="errors.password?.[0]" <!--Error goes here-->
  />
</div>
```

### Composables

Composables are like services but stateful. You can use them for most of the business logic (at least thats what ChatGPT said). There should be one composable for each entity (like `useCar` or `useUser`) to make them well organized. If you have a better idea on how to encapsulate business logic, create an issue or write to me on discord :)

When writing api calls I try to have one method for the API call only and one which handles all the other stuff like in the example below. You can either implement your stuff like that too or come up with a more elegant solution. 

```typescript
const registerUser = async (user: UserRegister) => {
      await postRegisterData(user);

      // turn UserRegister into UserLogin
      const userLogin: UserLogin = {
        email: user.email,
        password: user.password
      }

      const data = await postLoginData(userLogin);
      authStore.setAccessToken(data.access_token);
      showToast('success', "Registrierung erfolgreich!")
      router.push('/'); // Navigate to home page
  }

  const postRegisterData = async (user: UserRegister) => {
    try {
      const response = await api.post(
        '/users/signup',
        user
      )
      return response.data
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          console.error('Axios Error:', error.response?.data || error.message)
        } else {
          console.error('Unbekannter Fehler:', error)
        }
        throw error
  }
  }
```

We also have a composable `useToaster.ts` for displaying toast notifications (pop ups at the bottom of the screen). At the moment this is done using a third party library and is kind of trash. Just use it for now as it is, I will try to create a more elegant solution later. 

### State management

State management is done using **pinia**. Stores go in the `./stores` directory. 

At the moment we have 1 store to handle the authentication and make the access token available locally. It is currently saved as plain text in the localstorage, if you want you can implement a way of storing it in a more secure way. 


### Types

Add types for entities like user, car, drive, etc. in the `./types` directory. 


### Code quality

The project uses ESLint for code quality. Make sure to run the linter before committing changes, otherwise the CI Pipeline will fail:

```bash
npm run lint:check
```
