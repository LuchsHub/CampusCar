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
npm run lint
```

## Project Structure

```
src/
├── assets/        # Static assets like images and global styles
├── components/    # Reusable Vue components
├── composables/   # Vue composition functions
├── layouts/       # Layout components
├── router/        # Vue Router configuration
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

The project uses ESLint for code quality. Make sure to run the linter before committing changes:

```bash
npm run lint
```

## Building for Production

To build the project for production:

```bash
npm run build
```

The built files will be in the `dist` directory.
