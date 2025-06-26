# CampusCar Frontend

This is the frontend application for the CampusCar project, built with Vue 3, TypeScript, and Vite.

## Project Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint:check
```

## Project Structure

```
src/
├── assets/        # Static assets like images and global styles
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

## Features

- Vue 3 with Composition API
- TypeScript support
- Vue Router for navigation
- ESLint for code quality
- Vite for fast development and building

## Development

Frontend development happens on the branch `frontend_dev`. If you want to add a feature, create a **new branch** based on this branch and PR when finished. New branches follow the following naming conventions: `feature/<issue_no>_<feature_name>`. For example: `feature/5_login_view`.

The project uses ESLint for code quality. Make sure to run the linter before committing changes:

```bash
npm run lint:check
```

## Building for Production

To build the project for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

## State Management with Pinia

This project uses [Pinia](https://pinia.vuejs.org/) for state management.

### Setup
Pinia is already integrated in `src/main.ts`:
```ts
import { createPinia } from 'pinia'
const pinia = createPinia()
app.use(pinia)
```

### Example Store: Counter
A basic example store is provided at `src/stores/counter.ts`:
```ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  actions: {
    increment() { this.count++ },
    decrement() { this.count-- }
  }
})
```

### Usage Example in a Component
```vue
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
</script>

<template>
  <div>
    <p>Count: {{ counter.count }}</p>
    <button @click="counter.increment">Increment</button>
    <button @click="counter.decrement">Decrement</button>
  </div>
</template>
```

- Access state via `counter.count`
- Call actions via `counter.increment()` and `counter.decrement()`

For more advanced usage, see the [Pinia documentation](https://pinia.vuejs.org/).

## API Usage Example

This project uses a centralized [Axios](https://axios-http.com/) instance for all HTTP requests, located at `src/services/api.ts`.

### Example: GET Request
```ts
import api from '@/services/api'

async function fetchItems() {
  try {
    const response = await api.get('/items')
    console.log(response.data)
  } catch (error) {
    // Handle error
    console.error(error)
  }
}
```

### Example: POST Request
```ts
import api from '@/services/api'

async function createItem(itemData) {
  try {
    const response = await api.post('/items', itemData)
    console.log(response.data)
  } catch (error) {
    // Handle error
    console.error(error)
  }
}
```

- The base URL is set in `src/services/api.ts` and can be configured via the `VITE_API_BASE_URL` environment variable.
- All requests use JSON by default and support interceptors for authentication or error handling.

For more advanced usage, see the [Axios documentation](https://axios-http.com/).
